import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel, Field
from functools import lru_cache
from pydantic_settings import BaseSettings 
import urllib.parse
load_dotenv()

HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")

PORT = os.environ.get("MAIL_PORT", 465)

class MailBody(BaseModel):
    to: List[str]
    subject: str
    body: str

class AppConfig(BaseSettings):
    NAME: str = Field("FastAPI App", env="APP_NAME")
    ENV: str = Field("development", env="APP_ENV")
    DEBUG: bool = Field(True, env="DEBUG")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")
    API_PREFIX: str = Field("/api", env="API_PREFIX")

class StownConfig(BaseSettings):
    LOGIN: str = Field(os.environ.get("STOWN_LOGIN"))
    PASSWORD: str = Field(os.environ.get("STOWN_PASSWORD"))
    CLIENT_ID: str = Field(os.environ.get("STOWN_CLIENT_ID"))
    CLIENT_SECRET: str = Field(os.environ.get("STOWN_CLIENT_SECRET"))
    SCOPE: str = Field(os.environ.get("STOWN_SCOPE"))
    
    AUTH_URL: str = 'https://stown.ooo/api/acount/auth/token/'
    DEVICES_URL: str = "https://stown.ooo/api/control/box/" 
    
    @property
    def build_login_data(self) -> object:
        return {
          'grant_type': 'password',
          'username': self.LOGIN,
          'password': self.PASSWORD,
          'client_id': self.CLIENT_ID,
          'client_secret': self.CLIENT_SECRET,
          'scope' : None
        }

class StownLocalConfig(BaseSettings):
    LOGIN: str = Field(os.environ.get("STOWN_LOCAL_LOGIN"))
    PASSWORD: str = Field(os.environ.get("STOWN_LOCAL_PASSWORD"))
    
    AUTH_URL: str = '/api/login'
    OPEN_URL: str = "/api/locks/open" 
    
    @property
    def build_login_data(self) -> object:
        return {
          'username': self.LOGIN,
          'password': self.PASSWORD,
        } 

class SecurityConfig(BaseSettings):
    API_KEY: str = Field('password-into-env', env="API_KEY")
    #ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    


class DatabaseConfig(BaseSettings):
    HOST: str = Field(os.environ.get("DB_HOST"))
    PORT: str = Field(os.environ.get("DB_PORT"))
    NAME: str = Field(os.environ.get("DB_NAME"))
    USER: str = Field(os.environ.get("DB_USER"))
    PASS: str = Field(os.environ.get("DB_PASS"))

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}"
                # postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}
                
class RedisConfig(BaseSettings):
    HOST: str = Field(os.environ.get("REDIS_HOST"))
    PORT: int = Field(os.environ.get("REDIS_PORT"))
    DB: str = Field(os.environ.get("REDIS_DB"))
    PASSWORD: str = Field(os.environ.get("REDIS_PASSWORD"))

    STOWN_KEY: str = 'stown_access_token'
    INTERCOMS_KEY : str = 'intercoms'
    
    @property
    def url(self) -> str:
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}/{self.PASSWORD}"

class MeasuresConfig(BaseSettings):
    TOKEN: str = Field(os.environ.get("MEASURES_TOKEN"))
    
    HOMES_URL: str = "https://measures.stown.ooo/api/dashboard/builds/{house_id}/homes"

class RabbitConfig(BaseSettings):
    USER: str = os.getenv("RABBIT_USER")
    PASSWORD: str = os.getenv("RABBIT_PASSWORD")
    HOST: str = os.getenv("RABBIT_HOST")
    PORT: str = os.getenv("RABBIT_PORT", 5672)
    VHOST: str= os.getenv("RABBIT_VHOST")
    QUEUE_OFF_INTERCOM: str = os.getenv("QUEUE_OFF_INTERCOM")
    QUEUE_CALLING: str = os.getenv("QUEUE_CALLING")
    vhost: str = PORT or "/"
    
    @property
    def url(self) -> str:
        return f"amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.VHOST}"

class Config(BaseSettings):
    app: AppConfig = AppConfig()
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    security: SecurityConfig = SecurityConfig()
    stown: StownConfig = StownConfig()
    stown_local: StownLocalConfig = StownLocalConfig()
    measures: MeasuresConfig = MeasuresConfig()
    rabbit: RabbitConfig = RabbitConfig()


@lru_cache
def get_config() -> Config:
    return Config()
