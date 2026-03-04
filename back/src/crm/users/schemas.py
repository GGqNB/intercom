from pydantic import BaseModel, Field
from typing import Annotated, Optional

# Схема для базовых полей пользователя
class BaseUser(BaseModel):
    name: str
    chat_id: str
    max_id: str
    flat: int
    house_id: int
    flat_stown: int

class ReadUser(BaseUser):
    id: int

class WriteUser(BaseUser):
    pass  

class FilterUser(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    chat_id: Annotated[Optional[str], Field(default=None)]
    max_id: Annotated[Optional[str], Field(default=None)]
    flat: Annotated[Optional[int], Field(default=None)]
    flat_stown: Annotated[Optional[int], Field(default=None)]
    house_id: Annotated[Optional[int], Field(default=None)]