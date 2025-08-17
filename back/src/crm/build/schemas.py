from typing import Annotated, Optional
from pydantic import BaseModel, Field
from src.crm.location.schemas import ReadCity

class BaseHouse(BaseModel):
    name: str
    geo_adress: str
    flat_count: int

class ReadHouse(BaseHouse):
    id:  int
    city: ReadCity


class WriteHouse(BaseHouse):
    city_id: int


class BaseEntry(BaseModel):
    name: str
    flat_first: int
    flat_last: int

class ReadEntry(BaseEntry):
    id:  int
    house: ReadHouse

class WriteEntry(BaseEntry):
    house_id: int

class FilterHouse(BaseModel):
    geo_adress: Annotated[Optional[str], Field(default=None)]

class FilterEntry(BaseModel):
    name: Optional[str] = None
    geo_adress: Optional[str] = None
    house_id: Optional[int] = None