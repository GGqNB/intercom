import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel

load_dotenv()

HOST = os.environ.get("MAIL_HOST")
USERNAME = os.environ.get("MAIL_USERNAME")
PASSWORD = os.environ.get("MAIL_PASSWORD")

PORT = os.environ.get("MAIL_PORT", 465)
API_KEY = os.environ.get("API_KEY")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_HOST=os.environ.get("REDIS_HOST")
REDIS_PORT=os.environ.get("REDIS_PORT")
REDIS_DB=os.environ.get("REDIS_DB")
REDIS_PASSWORD=os.environ.get("REDIS_PASSWORD")

STOWN_LOGIN=os.environ.get("STOWN_LOGIN")
STOWN_PASSWORD=os.environ.get("STOWN_PASSWORD")
STOWN_CLIENT_ID=os.environ.get("STOWN_CLIENT_ID")
STOWN_CLIENT_SECRET=os.environ.get("STOWN_CLIENT_SECRET")
STOWN_SCOPE=os.environ.get("STOWN_SCOPE")

TOKEN_KEY = 'stown_access_token'
AUTH_URL = "https://stown.ooo/api/acount/auth/token/" 
DEVICES_URL = "https://stown.ooo/api/control/box/" 

class MailBody(BaseModel):
    to: List[str]
    subject: str
    body: str