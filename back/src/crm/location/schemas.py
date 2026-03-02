from pydantic import BaseModel


class BaseCity(BaseModel):
    name: str

class ReadCity(BaseCity):
    id:  int