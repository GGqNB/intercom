from collections import defaultdict
from typing import Dict, Optional
from fastapi import APIRouter, File, Form, UploadFile, status,  HTTPException, WebSocket, WebSocketDisconnect
import asyncio
from src.crm.logs.schemas import WriteCallLog
import threading
import json
from fastapi.security.api_key import APIKey
from fastapi import Depends, HTTPException
from src.auth import get_api_key, get_bot_key
from src.config import get_config
from starlette.status import HTTP_400_BAD_REQUEST
from src.intercom_connect.schemas import UserConnection
from src.intercom_connect.methods import *
from src.intercom_connect.helpers import *
from src.intercom_connect.schemas import BaseCallData, BlockDevice
from src.intercom_connect.methods import update_intercom_data, delete_room, send_push_endpoint
from src.crm.stown.crud import get_flat_by_house
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from json import JSONDecodeError
from src.crm.helper.image import compress_image_to_1mb, save_image
from src.crm.logs.crud import create_call_log
from src.rabbitmq import send_to_rabbitmq
from src.redis_client import redis_client


router_intercom_connect = APIRouter(prefix="", tags=["Работа с домофоном как с системой"])
conf = get_config()

# Словарь со списками соединений на каждого пользователя
connections: Dict[str, list] = defaultdict(list)
connections_lock = threading.Lock()

# Активные звонки
call_tasks = {}  # {apartment_number: {'task': Task, 'caller_ws': WebSocket, 'answered_by': str, 'call_ended_event': Event}}

def get_connections():
    active_calls = []
    with connections_lock:
        for apartment_number, call_data in call_tasks.items():
            caller_id = get_user_id(call_data['caller_ws'])
            answered_by = call_data.get('answered_by')
            status = "talking" if answered_by else "ringing"
            active_calls.append({
                "apartment_number": apartment_number,
                "status": status,
                "caller_id": caller_id,
                "answered_by": answered_by
            })
    return active_calls

async def cleanup_old_websockets():
    with connections_lock:
        for user_conns in connections.values():
            for conn in user_conns:
                try:
                    await conn.websocket.close()
                except:
                    pass
        connections.clear()

@router_intercom_connect.post("/open")
async def open_door(
    redis_open_token: str,
    bot_key: APIKey = Depends(get_bot_key),
    session: AsyncSession = Depends(get_async_session)
):
    key = f"{conf.redis.MAX_TOKEN_PREFIX}:{redis_open_token}"

    token_data_raw = redis_client.get(key)
    if not token_data_raw:
        raise HTTPException(status_code=400, detail="Токен недействителен или истёк")

    token_data = json.loads(token_data_raw)

    indentifier = token_data.get("indentifier")
    log_id = token_data.get("log_id")
    # house_id = token_data.get("house_id")
    # flat = token_data.get("flat_stown")

    if not indentifier:
        raise HTTPException(status_code=400, detail="Некорректный токен")

    intercom_ws = None
    with connections_lock:
        user_conns = connections.get(indentifier, [])
        for conn in user_conns:
            if conn.role == "intercom":
                intercom_ws = conn.websocket
                break

    if not intercom_ws:
        raise HTTPException(status_code=400, detail="Домофон не подключен")

    redis_client.delete(key)

    await safe_send_json(intercom_ws, {
        "type": "door_open",
        "log_id": log_id,
    })

    return {"message": "Команда на открытие отправлена"}

@router_intercom_connect.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    key = get_key(websocket)
    if key != conf.security.NEW_API_KEY:
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

    user_connection = UserConnection(websocket, user_id, flat_id, role)
    with connections_lock:
        # connections[user_id].append(user_connection)
        connections.setdefault(user_id, []).append(user_connection)
        print(f"Новое соединение: user_id={user_id}, квартира={flat_id}, роль={role}, всего соединений: {len(connections[user_id])}")

    

    try:
        while True:
            try:
                message = await websocket.receive_text()
            except WebSocketDisconnect:
                print(f"Клиент отключился: user_id={user_id}")
                break
            except Exception as e:
                print(f"Ошибка при приёме сообщения: {e}")
                break
            try:
                payload = json.loads(message)
            except json.JSONDecodeError:
                print("Not a JSON:", message)
                continue

            msg_type = payload.get("type")

            if msg_type == "ping":
                battery_level = payload.get("battery_level")
                battery_temp = payload.get("battery_temp")
                try:
                    battery_level = int(battery_level) if battery_level is not None else None
                    battery_temp = float(battery_temp) if battery_temp is not None else None
                except ValueError:
                    battery_level = None
                    battery_temp = None
                print(f"PING: battery_level={battery_level}, battery_temp={battery_temp}")
                await safe_send_json(websocket, {"type": "pong"})
                update_intercom_data(tech_name=user_id, battery_level=battery_level, battery_temp=battery_temp)

            elif msg_type == "call_ended_by_resident" and role == "resident":
                await end_call(flat_id, "resident", '')

    finally:
        with connections_lock:
            connections[user_id] = [conn for conn in connections[user_id] if conn.websocket != websocket]
            if not connections[user_id]:
                del connections[user_id]
            print(f"Соединение закрыто: user_id={user_id}, оставшиеся соединения: {len(connections.get(user_id, []))}")

@router_intercom_connect.post("/call")
async def call(call_data: BaseCallData, api_key: APIKey = Depends(get_api_key), session: AsyncSession = Depends(get_async_session)):
    flat_id = await get_flat_by_house(session, call_data.house_id, call_data.apartment_number)
    if flat_id is None:
        raise HTTPException(status_code=429, detail="Квартира не найдена, обратитесь к администратору")

    log_data = WriteCallLog(type="call", house_id=call_data.house_id, flat=flat_id, photo_url='', indentifier='')
    log = await create_call_log(session, log_data)
    
    token_room = await register_room(flat_id, call_data.hash_room)
    asyncio.create_task(send_push_endpoint(token_room, call_data.hash_room, call_data.indentifier, call_data.blockDevice, flat_id))
    intercom_ws = None
    with connections_lock:
        user_conns = connections.get(call_data.indentifier, [])
        if user_conns:
            intercom_ws = user_conns[0].websocket 
        if call_data.apartment_number in call_tasks:
            raise HTTPException(status_code=429, detail="Домофон занят, попробуйте позже (слишком много запросов)")
    if not intercom_ws:
        raise HTTPException(status_code=400, detail="Нет подключенного домофона.")

    asyncio.create_task(make_call(flat_id, call_data.apartment_number, 
                                  intercom_ws, call_data.hash_room, 
                                  call_data.blockDevice, log.id, token_room, call_data.indentifier))
    return {"message": f"Звонок инициирован в квартиру {call_data.apartment_number}."}

@router_intercom_connect.get("/answer_call/{flat_id}")
async def answer_call(flat_id: int, api_key: APIKey = Depends(get_api_key)):
    with connections_lock:
        if flat_id not in call_tasks:
            return {"message": f"Звонок в квартиру {flat_id} не найден."}

        answering_user_id = None
        for user_id, user_conns in connections.items():
            for conn in user_conns:
                if conn.role == "resident" and conn.flat_id == flat_id:
                    answering_user_id = user_id
                    break
            if answering_user_id:
                break

        if not answering_user_id:
            return {"message": "Нет жильцов онлайн в этой квартире."}

        call_tasks[flat_id]['answered_by'] = answering_user_id
        print(f"Звонок в квартиру {flat_id} принят пользователем {answering_user_id}.")

        try:
            await safe_send_json(call_tasks[flat_id]['caller_ws'], {"type": "call_answered", "flat_id": flat_id, "answered_by": answering_user_id})
        except Exception as e:
            print(f"Ошибка отправки уведомления домофону: {e}")

        return {"message": f"Звонок в квартиру {flat_id} принят."}

@router_intercom_connect.get("/abort_call/{flat_id}/{hash_room}")
async def abort_call(flat_id: int, hash_room: str, api_key: APIKey = Depends(get_api_key)):
    await end_call(flat_id, "aborted_by_intercom", hash_room)
    return {"message": f"Звонок в квартиру c id -{flat_id} отменен."}

@router_intercom_connect.get("/active_calls")
async def get_active_calls(api_key: APIKey = Depends(get_api_key)):
    return get_connections()

async def make_call(flat_id: int, apartment_number: int, caller_ws: WebSocket, hash_room: str, blockDevice: BlockDevice, log_id: int, token_room: str, indentifier: str):
    caller_id = get_user_id(caller_ws)
    print(f"Начат звонок в квартиру {apartment_number} (flat_id={flat_id}, инициатор: {caller_id}). hash_room: {hash_room} token_room:{token_room}")

    call_ended_event = asyncio.Event()
    call_tasks[flat_id] = {'task': asyncio.current_task(), 'caller_ws': caller_ws, 'answered_by': None, 'call_ended_event': call_ended_event, 'apartment_number': apartment_number}

    try:
        await safe_send_json(caller_ws, {"type": "call_started", "apartment": apartment_number, "flat_id": flat_id, "log_id": log_id, "token_room":token_room})

        with connections_lock:
            for user_conns in connections.values():
                for conn in user_conns:
                    if conn.role == "resident" and conn.flat_id == flat_id:
                        await safe_send_json(conn.websocket, {"type": "incoming_call", "from": "intercom", 
                                                              "apartment": apartment_number, "hash_room": hash_room, 
                                                              "block_device": blockDevice.model_dump() if blockDevice else None,
                                                              "token_room": token_room,
                                                              "indentifier": indentifier
                                                              })

        try:
            await asyncio.wait_for(call_ended_event.wait(), timeout=30)
            print(f"Звонок в квартиру {apartment_number} flat_id={flat_id} завершен событием.")
        except asyncio.TimeoutError:
            if call_tasks[flat_id]['answered_by'] is not None:
                print(f"Звонок в квартиру {apartment_number} flat_id={flat_id} был принят, таймаут игнорируется.")
                return
            await end_call(flat_id, "timeout", hash_room)
    except asyncio.CancelledError:
        print(f"Звонок в квартиру {apartment_number} flat_id={flat_id} был прерван.")
        await end_call(flat_id, "aborted", hash_room)
    finally:
        with connections_lock:
            if flat_id in call_tasks and call_tasks[flat_id]['answered_by'] is None:
                del call_tasks[flat_id]
                print(f"Задача звонка для квартиры {apartment_number} (flat_id={flat_id}) удалена из call_tasks.")

async def end_call(flat_id: int, reason: str, hash_room: str):
    try:
        if(hash_room != ''):
         await delete_room(hash_room)
    except:
        print('С удаление не прошло')
    with connections_lock:
        if flat_id not in call_tasks:
            print(f"Нет активного звонка для квартиры {flat_id}, нечего завершать.")
            return

        caller_ws = call_tasks[flat_id]['caller_ws']
        answered_by = call_tasks[flat_id]['answered_by']

        await safe_send_json(caller_ws, {"type": "call_ended", "apartment": flat_id, "reason": reason})
        print(f"Уведомлен домофон о завершении звонка в {flat_id} по причине: {reason}")

        for user_conns in connections.values():
            for conn in user_conns:
                if conn.role == "resident" and conn.flat_id == flat_id:
                    await safe_send_json(conn.websocket, {"type": "call_ended", "apartment": flat_id, "reason": reason})
                    print(f"Уведомлен жилец {conn.user_id} о завершении звонка в {flat_id} по причине: {reason}")

        call_tasks[flat_id]['call_ended_event'].set()
        try:
            call_tasks[flat_id]['task'].cancel()
        except Exception as e:
            print(f"Ошибка при отмене задачи: {e}")
        del call_tasks[flat_id]
        print(f"Задача звонка для квартиры {flat_id} удалена из call_tasks.")