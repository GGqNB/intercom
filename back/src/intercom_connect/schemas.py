from fastapi import WebSocket


class UserConnection:
    def __init__(self, websocket: WebSocket, user_id: str, apartment_number: int = None, role: str = "resident"):
        self.websocket = websocket
        self.user_id = user_id
        self.apartment_number = apartment_number
        self.role = role
