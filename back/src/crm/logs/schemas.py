from pydantic import BaseModel, Field
from datetime import datetime
from typing import Annotated, Optional


class BaseCallLog(BaseModel):
    type: str
    house_id: int
    flat: int
    photo_url: Optional[str]


class ReadCallLog(BaseCallLog):
    id: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }

class WriteCallLog(BaseCallLog):
    pass

class FilterCallLog(BaseModel):
    type: Annotated[Optional[str], Field(default=None)]
    house_id: Annotated[Optional[int], Field(default=None)]
    flat: Annotated[Optional[int], Field(default=None)]

    # фильтрация по дате
    date_from: Annotated[Optional[datetime], Field(default=None)]
    date_to: Annotated[Optional[datetime], Field(default=None)]