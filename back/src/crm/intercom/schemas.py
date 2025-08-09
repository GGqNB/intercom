from pydantic import BaseModel, Field
from src.crm.build.schemas import ReadEntry
from typing import Annotated, Optional

class BaseIntercom(BaseModel):
    name: str
    tech_name: str

class ReadIntercom(BaseIntercom):
    id:  int
    entry: ReadEntry

class WrhiteIntercom(BaseIntercom):
    entry_id: int

class FilterIntecom(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]