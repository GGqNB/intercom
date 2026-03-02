from typing import Dict, Optional
from fastapi import APIRouter, File, Form, UploadFile, status,  HTTPException, WebSocket, WebSocketDisconnect
import asyncio
from src.crm.logs.schemas import WriteCallLog
from src.crm.helper.stown import open_local_lock
import threading
import json
from fastapi.security.api_key import APIKey
from fastapi import Depends, HTTPException
from src.auth import get_api_key
from src.config import get_config
from starlette.status import HTTP_400_BAD_REQUEST
from src.intercom_connect.schemas import UserConnection
from src.intercom_connect.methods import *
from src.intercom_connect.helpers import *
from src.intercom_connect.schemas import BaseCallData, BlockDevice
from src.intercom_connect.methods import update_intercom_data
from src.crm.stown.crud import get_flat_by_house
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from json import JSONDecodeError
from src.crm.helper.image import compress_image_to_1mb, save_image
from src.crm.logs.crud import create_call_log
from src.factory.runners import send_to_rabbitmq
router_intercom_connect = APIRouter(
    prefix="",
    tags=["Работа с домофоном как с системой"]
)
conf = get_config()
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
    key = get_key(websocket)
    if key != conf.security.API_KEY:
        await websocket.close(code=1008, reason="Неверный key")
        return

    user_id = get_user_id(websocket)
    flat_id = get_flat_id(websocket)
    role = get_role(websocket)

    if not user_id or user_id == 'None':
        await websocket.close(code=1008, reason="Отсутствует user_id")
        return

    if role not in ("intercom", "resident", "courier"):
        await websocket.close(code=1008, reason="Неверная роль")
        return

    try:
        flat_id = int(flat_id) if flat_id else None
    except ValueError:
        await websocket.close(code=1008, reason="Неверный формат apartment_number")
        return

    # 🔥 СНАЧАЛА accept
    try:
        await websocket.accept()
    except Exception:
        return

    user_connection = UserConnection(websocket, user_id, flat_id, role)

    with connections_lock:
        old_conn = connections.get(user_id)
        if old_conn:
            try:
                await old_conn.websocket.close()
            except:
                pass
        connections[user_id] = user_connection

    print(f"Новое соединение: {user_id}")

    try:
        while True:
            try:
                message = await websocket.receive_text()
            except WebSocketDisconnect:
                print(f"Клиент отключился: {user_id}")
                break
            except Exception as e:
                print(f"Ошибка при приёме сообщения: {e}")
                break  

            try:
                payload = json.loads(message)
            except json.JSONDecodeError:
                continue

            msg_type = payload.get("type")

            if msg_type == "ping":
                await safe_send_json(websocket, {"type": "pong"})

            elif msg_type == "call_ended_by_resident" and role == "resident":
                await end_call(user_connection.flat_id, "resident")

    finally:
        with connections_lock:
            connections.pop(user_id, None)

        try:
            await websocket.close()
        except:
            pass

        print(f"Соединение закрыто: {user_id}")


# @router_intercom_connect.post("/call")
# async def call(
#     house_id: int = Form(...),
#     apartment_number: int = Form(...),
#     hash_room: str = Form(...),
#     indentifier: str = Form(...),
#     blockDevice: Optional[str] = Form(None),
#     photo: Optional[UploadFile] = File(None),
#     api_key: APIKey = Depends(get_api_key),
#     session: AsyncSession = Depends(get_async_session),
#     ):
#      photo_path = None
#      if photo:
#         file_bytes = await photo.read()
#         compressed_bytes = compress_image_to_1mb(file_bytes)
#         photo_path = save_image(compressed_bytes)
#         print(photo_path)
        
#      with connections_lock:
#          if apartment_number in call_tasks:
#             raise HTTPException(status_code=429, detail="Домофон занят, попробуйте позже (слишком много запросов)")
#          else:
#            intercom_ws = next((conn.websocket for conn in connections.values() if conn.user_id == indentifier), None)
#            if not intercom_ws:
#             raise HTTPException(status_code=400, detail="Нет подключенного домофона.")
#            flat_id = await get_flat_by_house(session, house_id, apartment_number)
#            if flat_id is None:
#              raise HTTPException(status_code=429, detail="Квартира не найдена, обратитесь к администратору")  
#            asyncio.create_task(make_call(flat_id, apartment_number,  intercom_ws, hash_room, blockDevice))
           
#            log_data = WriteCallLog(
#                type="call",
#                house_id=house_id,
#                flat=apartment_number,
#                photo_url=photo_path
#            )
#            await create_call_log(session, log_data)
#            try:
#               await call_to_max()
#            except:
#                print('Сообщеение в MAX не ушло')
           
#            return {"message": f"Звонок инициирован в квартиру {apartment_number}."}
@router_intercom_connect.post("/call")
async def call(call_data: BaseCallData, api_key: APIKey = Depends(get_api_key),  session: AsyncSession = Depends(get_async_session),):
     flat_id = await get_flat_by_house(session, call_data.house_id, call_data.apartment_number)
     if flat_id is None:
        raise HTTPException(status_code=429, detail="Квартира не найдена, обратитесь к администратору")  
     print(flat_id)
     
     log_data = WriteCallLog(
               type="call",
               house_id=call_data.house_id,
               flat=flat_id,
               photo_url=''
           )
     log = await create_call_log(session, log_data)   

     with connections_lock:
         if call_data.apartment_number in call_tasks:
            raise HTTPException(status_code=429, detail="Домофон занят, попробуйте позже (слишком много запросов)")
         else:
           intercom_ws = next((conn.websocket for conn in connections.values() if conn.user_id == call_data.indentifier), None)
           if not intercom_ws:
            raise HTTPException(status_code=400, detail="Нет подключенного домофона.")
           asyncio.create_task(make_call(flat_id, call_data.apartment_number,  intercom_ws, call_data.hash_room, call_data.blockDevice, log.id))
     return {"message": f"Звонок инициирован в квартиру {call_data.apartment_number}."}        
        #    log_data = WriteCallLog(
        #        type="call",
        #        house_id=call_data.house_id,
        #        flat=call_data.apartment_number,
        #        photo_url=''
        #    )
        #    await create_call_log(session, log_data)
        #    try:
        #       await call_to_max()
        #    except:
        #        print('Сообщеение в MAX не ушло')

@router_intercom_connect.get("/answer_call/{flat_id}")
async def answer_call(flat_id: int,  api_key: APIKey = Depends(get_api_key)):
     with connections_lock:
        if flat_id in call_tasks:
            answering_user_id = next((user_id for user_id, conn in connections.items() if conn.flat_id == flat_id and conn.role == "resident"), None)

            if not answering_user_id:
                return {"message": "Нет жильцов онлайн в этой квартире."}

            call_tasks[flat_id]['answered_by'] = answering_user_id
            print(f"Звонок в квартиру {flat_id} принят пользователем {answering_user_id}.")

            try:
                await safe_send_json(call_tasks[flat_id]['caller_ws'], {"type": "call_answered", "flat_id": flat_id, "answered_by": answering_user_id})
            except Exception as e:
                print(f"Ошибка отправки уведомления домофону: {e}")

            return {"message": f"Звонок в квартиру {flat_id} принят."}
        else:
            return {"message": f"Звонок в квартиру {flat_id} не найден."}

@router_intercom_connect.get("/abort_call/{flat_id}")
async def abort_call(flat_id: int, api_key: APIKey = Depends(get_api_key)):
    await end_call(flat_id, "aborted_by_intercom")
    return {"message": f"Звонок в квартиру c id -{flat_id} отменен."}

@router_intercom_connect.get("/valid-key/{key}")
async def login(key: str):
    if key == conf.security.API_KEY:
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
            data = await websocket.receive_json()  
            print(f"Received from {client_id}: {data}")

            recipient_id = data.get("to") 
            if recipient_id and recipient_id in active_connections:
                recipient_socket = active_connections[recipient_id]
                await recipient_socket.send_json(data) 
                print(f"Sent to {recipient_id}: {data}")
            else:
                print(f"Recipient {recipient_id} not found")
                await websocket.send_json({"error": "Recipient not found"}) 

    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
        del active_connections[client_id] 
    except Exception as e:
        print(f"Error for client {client_id}: {e}")
        del active_connections[client_id]


async def make_call(
    flat_id: int,
    apartment_number: int,
    caller_ws: WebSocket,
    hash_room: str,
    blockDevice: BlockDevice,
    log_id = int,
):
    caller_id = get_user_id(caller_ws)
    print(f"Начат звонок в квартиру {apartment_number} (flat_id={flat_id}, инициатор: {caller_id}). hash_room: {hash_room}")

    call_ended_event = asyncio.Event()

    call_tasks[flat_id] = {
        'task': asyncio.current_task(),
        'caller_ws': caller_ws,
        'answered_by': None,
        'call_ended_event': call_ended_event,
        'apartment_number': apartment_number
    }
    print(call_tasks[flat_id])

    try:
        await safe_send_json(caller_ws, {
            "type": "call_started",
            "apartment": apartment_number,
            "flat_id": flat_id,
            "log_id": log_id
        })

        # Оповещаем жильцов
        with connections_lock:
            for user_id, user_connection in connections.items():
                print('----------------------------')
                print(getattr(user_connection, "flat_id", None))
                if getattr(user_connection, "role", None) == "resident" and getattr(user_connection, "flat_id", None) == flat_id:
                    await safe_send_json(user_connection.websocket, {
                        "type": "incoming_call",
                        "from": "intercom",
                        "apartment": apartment_number,
                        "hash_room": hash_room,
                        "block_device":  blockDevice.model_dump() if blockDevice else None,
                    })

        # Ждем окончания звонка или таймаута
        try:
            await asyncio.wait_for(call_ended_event.wait(), timeout=20)
            print(f"Звонок в квартиру {apartment_number} flat_id={flat_id} завершен событием.")
        except asyncio.TimeoutError:
            with connections_lock:
                if call_tasks[flat_id]['answered_by'] is not None:
                    print(f"Звонок в квартиру {apartment_number} flat_id={flat_id} был принят, таймаут игнорируется.")
                    return
            await end_call(flat_id, "timeout")

    except asyncio.CancelledError:
        print(f"Звонок в квартиру {apartment_number} flat_id={flat_id} был прерван.")
        await end_call(flat_id, "aborted")

    finally:
        with connections_lock:
            if flat_id in call_tasks:
                if call_tasks[flat_id]['answered_by'] is None:
                    del call_tasks[flat_id]
                    print(f"Задача звонка для квартиры {apartment_number} (flat_id={flat_id}) удалена из call_tasks.")
                else:
                    print(f"Задача звонка для квартиры {apartment_number} (flat_id={flat_id}) НЕ удалена из call_tasks, answered_by: {call_tasks[flat_id].get('answered_by')}")
        print(f"Завершена задача звонка для квартиры {apartment_number} (flat_id={flat_id}).")

      

async def end_call(flat_id: int, reason: str):
    """Завершает звонок и уведомляет все стороны."""
    with connections_lock:
        
        if flat_id in call_tasks:
            caller_ws = call_tasks[flat_id]['caller_ws']
            answered_by = call_tasks[flat_id]['answered_by']

            # Уведомляем домофон
            await safe_send_json(caller_ws, {"type": "call_ended", "apartment": flat_id, "reason": reason})
            # await safe_send_json(caller_ws, {"type": "call_ended", "apartment": apartment_number, "flat_id":flat_id, "reason": reason})
            print(f"Уведомлен домофон о завершении звонка в {flat_id} по причине: {reason}")

            for user_id, user_connection in connections.items():
                if user_connection.role == "resident" and user_connection.flat_id == flat_id:
                    await safe_send_json(user_connection.websocket, {"type": "call_ended", "apartment": flat_id, "reason": reason})
                    print(f"Уведомлен жилец {user_id} о завершении звонка в {flat_id} по причине: {reason}")

            call_tasks[flat_id]['call_ended_event'].set()

            try:
                call_tasks[flat_id]['task'].cancel()
            except Exception as e:
                print(f"Ошибка при отмене задачи: {e}")

            del call_tasks[flat_id]
            print(f"Задача звонка для квартиры {flat_id} удалена из call_tasks.")
        else:
            print(f"Нет активного звонка для квартиры {flat_id}, нечего завершать.")
            