
from typing import Optional
from fastapi import WebSocket
from pydantic import BaseModel
from typing import Optional, Union, Any, Dict

class BlockDevice(BaseModel):
    id: int
    name: str
    owner_id: str
    addr: str
    status: int
    is_owner: bool
    id_permission: Optional[Union[int, str]]  # может быть int или str
    is_one_access: bool
    rules: list
    type: str
    photo_url: Optional[str]
    owner_short_name: str
    is_time_access: bool
    has_access: Optional[Union[bool, str]]  # может быть bool или str
    time_access: Optional[Union[Dict, str]]  # может быть dict или str
    geo_lat: float
    geo_lon: float
    kladr_id: str

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


