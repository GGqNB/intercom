
from typing import List, Optional
from fastapi import WebSocket
from pydantic import BaseModel
from typing import Optional, Union, Any, Dict

class BlockDevice(BaseModel):
    model_config = {
        "extra": "allow"  # игнорировать лишние поля
    }
    id: Optional[int] = None
    name: Optional[str] = None
    owner_id: Optional[str] = None
    addr: Optional[str] = None
    status: Optional[int] = None
    is_owner: Optional[bool] = None

    id_permission: Optional[Union[int, str]] = None
    is_one_access: Optional[bool] = None

    rules: Optional[List[Any]] = None
    type: Optional[str] = None

    photo_url: Optional[str] = None
    owner_short_name: Optional[str] = None

    is_time_access: Optional[bool] = None
    has_access: Optional[Union[bool, str]] = None

    time_access: Optional[Union[Dict[str, Any], str]] = None

    geo_lat: Optional[float] = None
    geo_lon: Optional[float] = None

    kladr_id: Optional[str] = None

class BaseCallData(BaseModel):
    house_id: Optional[int] = None
    apartment_number: int
    hash_room: str
    indentifier: str
    blockDevice: Optional[BlockDevice] = None

class UserConnection:
    def __init__(self, websocket: WebSocket, user_id: str, flat_id: int = None, role: str = "resident"):
        self.websocket = websocket
        self.user_id = user_id
        self.flat_id = flat_id
        self.role = role


# class UserConnection:
#     def __init__(self, websocket: WebSocket, user_id: str, apartment_number: int = None, role: str = "resident"):
#         self.websocket = websocket
#         self.user_id = user_id
#         self.apartment_number = apartment_number
#         self.role = role


