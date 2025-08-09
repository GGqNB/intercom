from fastapi import WebSocket

def get_user_id(websocket: WebSocket):
    return websocket.query_params.get("user_id")

def get_key(websocket: WebSocket):
    return websocket.query_params.get("key")


def get_hash_room(websocket: WebSocket):
    return websocket.query_params.get("hash_room")


def get_apartment_number(websocket: WebSocket):
    return websocket.query_params.get("apartment_number")


def get_role(websocket: WebSocket):
    return websocket.query_params.get("role")

async def safe_send_json(websocket: WebSocket, data: dict):
    """Обертка для отправки JSON, обрабатывающая возможные ошибки."""
    try:
        await websocket.send_json(data)
    except Exception as e:
        print(f"Ошибка при отправке сообщения {data} через WebSocket: {e}")