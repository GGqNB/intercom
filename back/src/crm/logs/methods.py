import datetime

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta, timezone

from src.crm.logs.models import CallLog
from src.config import get_config
import json
from src.crm.logs.schemas import ReadCallLog, WriteCallLog, FilterCallLog
from src.redis_client import redis_client
from src.crm.intercom.models import Intercom
from typing import Any, Dict
import secrets
import asyncio
from src.database import async_session_maker
from src.factory.runners import send_to_rabbitmq
conf = get_config()




def get_logs_intercoms():
    intercoms_json = redis_client.get(conf.redis.INTERCOMS_KEY)
    return json.loads(intercoms_json) if intercoms_json else []

def intercom_to_dict(ic: Intercom) -> Dict[str, Any]:
                return {
                    "id": ic.id,
                    "name": ic.name,
                    "tech_name": ic.tech_name,
                    "entry_id": ic.entry_id,
                    "entry": {
                        "id": ic.entry.id,
                        "name": ic.entry.name,
                        "flat_first": ic.entry.flat_first,
                        "flat_last": ic.entry.flat_last,
                        "house_id": ic.entry.house_id,
                    } if getattr(ic, "entry", None) else None,
                }


def generate_token() -> str:
    return secrets.token_urlsafe(32)

async def create_action_token(data: Dict[str, Any]) -> str:
    token = generate_token()
    key = f"{conf.redis.MAX_TOKEN_PREFIX}:{token}"

    redis_client.set(
        key,
        json.dumps(data),
        ex=conf.redis.MAX_TOKEN_TTL
    )

    return token

TIMEZONE_OFFSET = -5 
TIMEZONE = timezone(timedelta(hours=TIMEZONE_OFFSET))
QUEUE_OFF_INTERCOM = f"{conf.rabbit.QUEUE_OFF_INTERCOM}"

async def handle_call_log_event(data: WriteCallLog):
    if data.type != "crash":
        return

    try:
        if not data.indentifier:
            return

        async with async_session_maker() as session:
            query = (
                select(Intercom)
                .options(selectinload(Intercom.entry))
                .where(Intercom.tech_name == data.indentifier)
            )

            result = await session.execute(query)
            intercom: Intercom | None = result.scalar_one_or_none()

        current_time_utc = datetime.now(timezone.utc)
        current_time = current_time_utc.astimezone(TIMEZONE) 
        
        message = {
            "event": "intercom_crash",
            "tech_name": data.indentifier,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": data.model_dump(),
            "intercom_data": intercom_to_dict(intercom) if intercom else None,
        }
        print(message)
        await send_to_rabbitmq(message, queue_name=QUEUE_OFF_INTERCOM)

    except Exception as e:
        print(f"Ошибка обработки события: {e}")