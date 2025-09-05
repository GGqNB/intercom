from typing import Dict
from fastapi import APIRouter, FastAPI, Form, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, Request
import asyncio
import threading
import json
from fastapi.security.api_key import APIKey
from fastapi import Depends, HTTPException
from src.auth import get_api_key
from src.config import API_KEY
from starlette.status import HTTP_400_BAD_REQUEST
from src.intercom_connect.schemas import UserConnection
from src.intercom_connect.methods import *
from src.intercom_connect.helpers import *
from src.intercom_connect.schemas import BaseCallData, BlockDevice

router_intercom_connect = APIRouter(
    prefix="",
    tags=["Работа с домофоном как с системой"]
)

connections = {}
connections_lock = threading.Lock()

call_tasks = {}  # {apartment_number: {'task': Task, 'caller_ws': WebSocket, 'answered_by': str, 'call_ended_event': Event}}

def get_connections():
    active_calls = []
    with connections_lock:
        for apartment_number, call_data in call_tasks.items():
            caller_id = get_user_id(call_data['caller_ws'])  
            answered_by = call_data.get('answered_by')

            if answered_by:
                status = "talking"
            else:
                status = "ringing"

            active_calls.append({
                "apartment_number": apartment_number,
                "status": status,
                "caller_id": caller_id,
                "answered_by": answered_by
            })
    return active_calls



@router_intercom_connect.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # print(API_KEY)
    key = get_key(websocket)
    if key != API_KEY:
        await websocket.close(code=1008, reason="Неверный key")
        return
    user_id = get_user_id(websocket)
    apartment_number = get_apartment_number(websocket)
    role = get_role(websocket)

    if not user_id or user_id=='None':
        await websocket.close(code=1008, reason="Отсутствует user_id")
        return

    if role not in ("intercom", "resident", "courier"):
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
            if data.lower() == "ping":  # Case-insensitive comparison
                await safe_send_json(websocket, {"type": "pong"})  # Использовать safe_send_json
            elif data == "call_ended_by_resident" and role == "resident":
                apartment = user_connection.apartment_number
                await end_call(apartment, "resident")
            # else:
            #     print(f"Получено сообщение: {data} от user_id {user_id}")

    except WebSocketDisconnect:
        print(f"Клиент отключился: user_id={user_id}")
    finally:
        with connections_lock:
            if user_id in connections:  # Проверка перед удалением
                del connections[user_id]
        print(f"Соединение закрыто: user_id={user_id}, соединения={connections}")



# @router_intercom_connect.get("/call/{apartment_number}/{hash_room}/{indentifier}")
# async def call(apartment_number: int,
#                hash_room: str, 
#                indentifier: str,
#                api_key: APIKey = Depends(get_api_key),
#                ):
#      with connections_lock:
#          if apartment_number in call_tasks:
#             raise HTTPException(status_code=429, detail="Домофон занят, попробуйте позже (слишком много запросов)")
#          else:
#            intercom_ws = next((conn.websocket for conn in connections.values() if conn.user_id == indentifier), None)
#            if not intercom_ws:
#             raise HTTPException(status_code=400, detail="Нет подключенного домофона.")  
#            asyncio.create_task(make_call(apartment_number, intercom_ws, hash_room))
#            return {"message": f"Звонок инициирован в квартиру {apartment_number}."}

@router_intercom_connect.post("/call")
async def call(call_data: BaseCallData, api_key: APIKey = Depends(get_api_key)):
     with connections_lock:
         if call_data.apartment_number in call_tasks:
            raise HTTPException(status_code=429, detail="Домофон занят, попробуйте позже (слишком много запросов)")
         else:
           intercom_ws = next((conn.websocket for conn in connections.values() if conn.user_id == call_data.indentifier), None)
           if not intercom_ws:
            raise HTTPException(status_code=400, detail="Нет подключенного домофона.")  
           asyncio.create_task(make_call(call_data.apartment_number, intercom_ws, call_data.hash_room, call_data.blockDevice))
           return {"message": f"Звонок инициирован в квартиру {call_data.apartment_number}."}
        

@router_intercom_connect.get("/answer_call/{apartment_number}")
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

@router_intercom_connect.get("/abort_call/{apartment_number}")
async def abort_call(apartment_number: int, api_key: APIKey = Depends(get_api_key)):
    await end_call(apartment_number, "aborted_by_intercom")
    return {"message": f"Звонок в квартиру {apartment_number} отменен."}

@router_intercom_connect.get("/valid-key/{key}")
async def login(key: str):
    if key == API_KEY:
        return { "key": key}   
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Неправильный токен"
        )



@router_intercom_connect.get("/active_calls")
async def get_active_calls(api_key: APIKey = Depends(get_api_key)):
    
   
    return get_connections()


active_connections: Dict[str, WebSocket] = {}

@router_intercom_connect.websocket("/ws/test/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    active_connections[client_id] = websocket
    print(f"Client {client_id} connected")
    try:
        while True:
            data = await websocket.receive_json()  # Получаем JSON данные от клиента
            print(f"Received from {client_id}: {data}")

            # Обработка полученных данных
            recipient_id = data.get("to") # предполагаем, что клиент шлет сообщение с указанием ID получателя
            if recipient_id and recipient_id in active_connections:
                recipient_socket = active_connections[recipient_id]
                await recipient_socket.send_json(data) # пересылаем сообщение получателю
                print(f"Sent to {recipient_id}: {data}")
            else:
                print(f"Recipient {recipient_id} not found")
                await websocket.send_json({"error": "Recipient not found"}) # сообщаем об ошибке

    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
        del active_connections[client_id] # удаляем соединение
    except Exception as e:
        print(f"Error for client {client_id}: {e}")
        del active_connections[client_id]


async def make_call(apartment_number: int, caller_ws: WebSocket, hash_room: str, blockDevice:BlockDevice, api_key: APIKey = Depends(get_api_key)):

    caller_id = get_user_id(caller_ws)
    print(f"Начат звонок в квартиру {apartment_number} (инициатор: {caller_id}). hash_room: {hash_room}")
    call_ended_event = asyncio.Event()
    call_tasks[apartment_number] = {'task': asyncio.current_task(), 'caller_ws': caller_ws, 'answered_by': None, 'call_ended_event': call_ended_event}

    try:
        await safe_send_json(caller_ws, {"type": "call_started", "apartment": apartment_number})

        with connections_lock:
            for user_id, user_connection in connections.items():
                if user_connection.role == "resident" and user_connection.apartment_number == apartment_number:
                    await safe_send_json(user_connection.websocket, 
                            {"type": "incoming_call", "from": "intercom", "apartment": apartment_number, "hash_room": hash_room, "block_device": str(blockDevice)})
                    # print("incoming_call", apartment_number)

        try:
            await asyncio.wait_for(call_ended_event.wait(), timeout=10)  # Ожидаем завершения или ответа
            print(f"Звонок в квартиру {apartment_number} завершен событием.")

        except asyncio.TimeoutError:
            with connections_lock:
                if call_tasks[apartment_number]['answered_by'] is not None:
                    print(f"Звонок в {apartment_number} был принят, таймаут игнорируется.")
                    return  # ВАЖНО: Не завершаем задачу, если звонок был принят

            # print(f"Время ожидания истекло для звонка в квартиру {apartment_number}.")
            await end_call(apartment_number, "timeout")
            # print("timeout", apartment_number)

    except asyncio.CancelledError:
        print(f"Звонок в квартиру {apartment_number} был прерван.")
        await end_call(apartment_number, "aborted")

    finally:
        with connections_lock:
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
            print('__________________________-')
            print(call_tasks)
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