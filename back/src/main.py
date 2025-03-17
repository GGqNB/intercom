
from fastapi import FastAPI, Form, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.schemas import BaseDataPushSchemas
import asyncio
from fastapi.middleware.cors import CORSMiddleware
import threading
import json
from fastapi.security.api_key import APIKey
from fastapi import Depends, HTTPException
from src.auth import get_api_key
from src.config import API_KEY
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.status import HTTP_403_FORBIDDEN


app = FastAPI()

origins = [
    "http://localhost:9000",
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:9000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

MAIL_HOST = ""
MAIL_USERNAME = ""
MAIL_PASSWORD = ""
MAIL_PORT = 0


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/send_email")
async def send_email(data: BaseDataPushSchemas, api_key: APIKey = Depends(get_api_key)):
    try:
        msg = MIMEMultipart()
        msg["From"] = MAIL_USERNAME
        msg["To"] = data.to
        msg["Subject"] = data.subject
        msg.attach(MIMEText(data.message, "plain"))

        with smtplib.SMTP_SSL(MAIL_HOST, MAIL_PORT) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(MAIL_USERNAME, data.to, msg.as_string())

        return {"message": "Письмо успешно отправлено!"}
    except Exception:
        raise HTTPException(status_code=500, detail='Произошла ошибка')


class UserConnection:
    def __init__(self, websocket: WebSocket, user_id: str, apartment_number: int = None, role: str = "resident"):
        self.websocket = websocket
        self.user_id = user_id
        self.apartment_number = apartment_number
        self.role = role


connections = {}
connections_lock = threading.Lock()

call_tasks = {}  # {apartment_number: {'task': Task, 'caller_ws': WebSocket, 'answered_by': str, 'call_ended_event': Event}}



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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print(API_KEY)
    key = get_key(websocket)
    print(key)
    if key != API_KEY:
        await websocket.close(code=1008, reason="Неверный key")
        return 
    user_id = get_user_id(websocket)
    apartment_number = get_apartment_number(websocket)
    role = get_role(websocket)

    if not user_id:
        await websocket.close(code=1008, reason="Отсутствует user_id")
        return

    if role not in ("domophone", "resident"):
        await websocket.close(code=1008, reason="Неверная роль")
        return

    try:
        apartment_number = int(apartment_number) if apartment_number else None
    except ValueError:
        await websocket.close(code=1008, reason="Неверный формат apartment_number")
        return

    user_connection = UserConnection(websocket, user_id, apartment_number, role)

    with connections_lock:
        connections[user_id] = user_connection
        print(f"Новое соединение: user_id={user_id}, квартира={apartment_number}, роль={role}, соединения={connections}")

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await safe_send_json(websocket, {"type": "pong"}) # Использовать safe_send_json
            elif data == "call_ended_by_resident" and role == "resident":
                apartment = user_connection.apartment_number
                await end_call(apartment, "resident")
            else:
                print(f"Получено сообщение: {data} от user_id {user_id}")

    except WebSocketDisconnect:
        print(f"Клиент отключился: user_id={user_id}")
    finally:
        with connections_lock:
            if user_id in connections:  # Проверка перед удалением
                del connections[user_id]
        print(f"Соединение закрыто: user_id={user_id}, соединения={connections}")

async def make_call(apartment_number: int, caller_ws: WebSocket, hash_room: str , api_key: APIKey = Depends(get_api_key)):
    caller_id = get_user_id(caller_ws)
    print(f"Начат звонок в квартиру {apartment_number} (инициатор: {caller_id}). hash_room: {hash_room}")
    call_ended_event = asyncio.Event()
    call_tasks[apartment_number] = {'task': asyncio.current_task(), 'caller_ws': caller_ws, 'answered_by': None, 'call_ended_event': call_ended_event}

    try:
        await safe_send_json(caller_ws, {"type": "call_started", "apartment": apartment_number})
        print('call_started', apartment_number)
        # Рассылка уведомлений жильцам
        with connections_lock:
            for user_id, user_connection in connections.items():
                if user_connection.role == "resident" and user_connection.apartment_number == apartment_number:
                    await safe_send_json(user_connection.websocket, {"type": "incoming_call", "from": "domophone", "apartment": apartment_number, "hash_room": hash_room})
                    print("incoming_call", apartment_number)

        try:
            await asyncio.wait_for(call_ended_event.wait(), timeout=10)  # Ожидаем завершения или ответа
            print(f"Звонок в квартиру {apartment_number} завершен событием.")

        except asyncio.TimeoutError:
            with connections_lock:
                if call_tasks[apartment_number]['answered_by'] is not None:
                    print(f"Звонок в {apartment_number} был принят, таймаут игнорируется.")
                    return  # ВАЖНО: Не завершаем задачу, если звонок был принят

            print(f"Время ожидания истекло для звонка в квартиру {apartment_number}.")
            await end_call(apartment_number, "timeout")
            print("timeout", apartment_number)

    except asyncio.CancelledError:
        print(f"Звонок в квартиру {apartment_number} был прерван.")
        await end_call(apartment_number, "aborted")

    finally:
        with connections_lock:
            # Удаляем задачу только если она не была принята и звонок еще существует
            if apartment_number in call_tasks and call_tasks[apartment_number]['answered_by'] is None:
                del call_tasks[apartment_number]
                print(f"Задача звонка для квартиры {apartment_number} удалена из call_tasks.")
            else:
                print(f"Задача звонка для квартиры {apartment_number} НЕ удалена из call_tasks, answered_by: {call_tasks[apartment_number].get('answered_by') if apartment_number in call_tasks else None}")
        print(f"Завершена задача звонка для квартиры {apartment_number}.")

async def end_call(apartment_number: int, reason: str):
    """Завершает звонок и уведомляет все стороны."""
    with connections_lock:
        if apartment_number in call_tasks:
            caller_ws = call_tasks[apartment_number]['caller_ws']
            answered_by = call_tasks[apartment_number]['answered_by']

            # Уведомляем домофон
            await safe_send_json(caller_ws, {"type": "call_ended", "apartment": apartment_number, "reason": reason})
            print(f"Уведомлен домофон о завершении звонка в {apartment_number} по причине: {reason}")

            # Уведомляем жильцов
            for user_id, user_connection in connections.items():
                if user_connection.role == "resident" and user_connection.apartment_number == apartment_number:
                    await safe_send_json(user_connection.websocket, {"type": "call_ended", "apartment": apartment_number, "reason": reason})
                    print(f"Уведомлен жилец {user_id} о завершении звонка в {apartment_number} по причине: {reason}")

            # Останавливаем ожидание
            call_tasks[apartment_number]['call_ended_event'].set()

            # Отменяем задачу, если она еще выполняется
            try:
                call_tasks[apartment_number]['task'].cancel()
            except Exception as e:
                print(f"Ошибка при отмене задачи: {e}")

            # Удаляем задачу
            del call_tasks[apartment_number]
            print(f"Задача звонка для квартиры {apartment_number} удалена из call_tasks.")
        else:
            print(f"Нет активного звонка для квартиры {apartment_number}, нечего завершать.")

@app.get("/call/{apartment_number}/{hash_room}")
async def call(apartment_number: int, hash_room: str, api_key: APIKey = Depends(get_api_key)):
    with connections_lock:
        domophone_ws = next((conn.websocket for conn in connections.values() if conn.role == "domophone"), None)

        if not domophone_ws:
            raise HTTPException(status_code=400, detail="Нет подключенного домофона.")

        asyncio.create_task(make_call(apartment_number, domophone_ws, hash_room))
        return {"message": f"Звонок инициирован в квартиру {apartment_number}."}

@app.get("/answer_call/{apartment_number}")
async def answer_call(apartment_number: int,  api_key: APIKey = Depends(get_api_key)):
    with connections_lock:
        if apartment_number in call_tasks:
            answering_user_id = next((user_id for user_id, conn in connections.items() if conn.apartment_number == apartment_number and conn.role == "resident"), None)

            if not answering_user_id:
                return {"message": "Нет жильцов онлайн в этой квартире."}

            call_tasks[apartment_number]['answered_by'] = answering_user_id
            print(f"Звонок в квартиру {apartment_number} принят пользователем {answering_user_id}.")

            try:
                await safe_send_json(call_tasks[apartment_number]['caller_ws'], {"type": "call_answered", "apartment": apartment_number, "answered_by": answering_user_id})
            except Exception as e:
                print(f"Ошибка отправки уведомления домофону: {e}")

            return {"message": f"Звонок в квартиру {apartment_number} принят."}
        else:
            return {"message": f"Звонок в квартиру {apartment_number} не найден."}

@app.get("/abort_call/{apartment_number}")
async def abort_call(apartment_number: int, api_key: APIKey = Depends(get_api_key)):
    await end_call(apartment_number, "aborted_by_domophone")
    return {"message": f"Звонок в квартиру {apartment_number} отменен."}

@app.get("/valid-key/{key}")
async def login(key: str):
    if key == API_KEY:
        return { "key": key}   
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Неправильный токен"
        )
