from pydantic import BaseModel, Field
from typing import Annotated, Optional

    
class ReadSHouse(BaseModel):
    id: int
    address: str
    
    
class ReadSFlat(BaseModel):
    id: int
    type: str
    number: int
    ext_number: str | None
    house_id: int
    
class FilterSHouse(BaseModel):
    address: Annotated[Optional[str], Field(default=None)]
    
class FilterSFlat(BaseModel):
    number: Annotated[Optional[int], Field(default=None)]
    house_id: Annotated[Optional[int], Field(default=None)]