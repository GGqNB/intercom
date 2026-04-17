
import json
from typing import Any, Dict, List, Optional
from src.crm.stown.methods import get_flat_number_by_ids
from fastapi import APIRouter, File, UploadFile, status
from src.crm.users.methods import get_users_by_house_and_flat
from src.rabbitmq import send_to_rabbitmq

from src.crm.logs.schemas import FilterCallLog, ReadCallLog, WriteCallLog
from src.crm.logs.crud import update_call_log, get_call_logs, delete_call_log, create_call_log, update_call_log_photo
from src.crm.logs.methods import get_logs_intercoms, intercom_to_dict
from src.config import get_config
from src.redis_client import redis_client
from src.database import get_async_session
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from src.crm.intercom.models import Intercom
from sqlalchemy import delete, func, insert, select
from sqlalchemy.orm import selectinload
from fastapi.security.api_key import APIKey
from src.auth import get_api_key, get_bot_key
from src.crm.intercom.models import Intercom
from src.crm.logs.methods import create_action_token

router_logs = APIRouter(
    prefix="/logs",
    tags=["Работа с логами"]
)

conf = get_config()


@router_logs.get("/clear-redis-intercoms")
async def clear_redis_intercoms(
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)

):
    try:
        redis_client.delete(conf.redis.INTERCOMS_KEY)
        return {
            "status" : "success"
        }  

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "args": e.args if hasattr(e, 'args') else None,
            }
        )
@router_logs.get("/redis-intercom")
async def redis_intercoms(
    session: AsyncSession = Depends(get_async_session),
    bot_key: APIKey = Depends(get_bot_key)
):
    try:
        query = select(Intercom).options(selectinload(Intercom.entry))
        result = await session.execute(query)
        intercom_objs: List[Intercom] = result.scalars().all()

        

        intercom_map: Dict[str, Dict[str, Any]] = {
            ic.tech_name: intercom_to_dict(ic) for ic in intercom_objs if ic.tech_name
        }

        logs: List[Dict[str, Any]] = get_logs_intercoms()
        merged_data: List[Dict[str, Any]] = []
        for item in logs:
            merged_item = dict(item) 
            tech = merged_item.get("tech_name")
            if tech and tech in intercom_map:
                merged_item["intercom"] = intercom_map[tech]
            else:

                merged_item["intercom"] = None
            merged_data.append(merged_item)

    
        return {
            "data": merged_data,
            "status": "success"
        }

    except Exception as e:
        return {"status": "error", "detail": str(e)}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "args": e.args if hasattr(e, 'args') else None,
            }
        )

@router_logs.get("/list", response_model=Page[ReadCallLog])
async def list_logs(
    filters: FilterCallLog = Depends(),
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    return await get_call_logs(session, filters)


@router_logs.post("", status_code=status.HTTP_201_CREATED)
async def add_log(
    new_log: WriteCallLog,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    created = await create_call_log(session, new_log)
    return {"data": created, "status": "success"}


@router_logs.put("/{log_id}")
async def edit_log(
    log_id: int,
    updated_log: WriteCallLog,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    updated = await update_call_log(session, log_id, updated_log)
    return {"data": updated, "status": "updated"}

QUEUE_CALLING = f"{conf.rabbit.QUEUE_CALLING}"

@router_logs.put("/{log_id}/rabbit/{indentifier}")
async def update_log_photo(
    log_id: int,
    indentifier: Optional[str] = None,
    photo: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    if not indentifier:
        print("Старый клиент — ничего не делаем")
        return {"status": "ok"}
    
    updated = await update_call_log_photo(session, indentifier, log_id, photo)
    log = updated["data"]

    try:
        users = await get_users_by_house_and_flat(
            session,
            log.house_id,
            log.flat
        )
        if not users:
            print('Юзеров нет, Rabbit не трогал')
            return updated
        flat_number = await get_flat_number_by_ids(
            session=session,
            house_id= log.house_id,
            flat_id=log.flat
        )
        try:
          open_token = await create_action_token({
           "log_id": log.id,
           "house_id": log.house_id,
           "flat_stown": log.flat,
           "indentifier": log.indentifier,
           })
        except Exception as e:
            print('В redis не смог записать, Rabbit не трогал')
            return updated
        
        users_payload = [
            {
                "id": user.id,
                "name": user.name,
                "chat_id": user.chat_id,
                "max_id": user.max_id
            }
            for user in users
        ]

        payload = {
            "id": log.id,
            "type": log.type,
            "house_id": log.house_id,
            "flat_stown": log.flat,
            "flat_number": flat_number,
            "photo_url": log.photo_url,
            "created_at": log.created_at.isoformat(),
            "open_token": open_token,
            "users": users_payload 
        }

        await send_to_rabbitmq(payload, QUEUE_CALLING)
        print('В rabbit ушло')
        print(open_token)
    except Exception as e:
        print("Ошибка отправки в RabbitMQ:", e)

    return updated

@router_logs.delete("/{log_id}")
async def remove_log(
    log_id: int,
    session: AsyncSession = Depends(get_async_session),
    api_key: APIKey = Depends(get_api_key)
):
    return await delete_call_log(session, log_id)