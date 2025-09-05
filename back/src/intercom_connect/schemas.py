
from typing import Optional
from fastapi import WebSocket
from pydantic import BaseModel

class BlockDevice(BaseModel):
       id: int
       addr: str
       has_access: Optional[str]  # Assuming 'str' is the intended type, otherwise use appropriate type
       id_permission: Optional[str] # Assuming 'str' is the intended type, otherwise use appropriate type
       is_one_access: bool
       is_owner: bool
       is_time_access: bool
       name: str
       owner_id: str
       owner_short_name: str
       photo_url: Optional[str]
       rules: list
       status: int
       time_access: Optional[str]
       type: str
    
class BaseCallData(BaseModel):
    apartment_number: int
    hash_room: str
    indentifier: str
    blockDevice: Optional[BlockDevice] = None


class UserConnection:
    def __init__(self, websocket: WebSocket, user_id: str, apartment_number: int = None, role: str = "resident"):
        self.websocket = websocket
        self.user_id = user_id
        self.apartment_number = apartment_number
        self.role = role


