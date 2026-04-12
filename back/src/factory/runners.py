from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import selectinload
from src.rabbitmq import send_to_rabbitmq
from src.database import get_async_session
from src.database import async_session_maker
from src.redis_client import redis_client
from src.config import get_config
from datetime import datetime, timedelta, timezone
from src.crm.intercom.models import Intercom
import json
from sqlalchemy import select
from typing import Any, Dict, List
from src.crm.logs.methods import intercom_to_dict
import asyncio
import aio_pika
from src.crm.helper.image import  delete_old_photos
conf = get_config()

TIMEZONE_OFFSET = -5 
TIMEZONE = timezone(timedelta(hours=TIMEZONE_OFFSET))

RABBIT_URL = f"{conf.rabbit.url}"  
QUEUE_OFF_INTERCOM = f"{conf.rabbit.QUEUE_OFF_INTERCOM}"


async def monitor_intercoms():
    print("📡 monitor_intercoms started")

    while True:
        try:
            intercoms_json = redis_client.get(conf.redis.INTERCOMS_KEY)
            current_intercoms = json.loads(intercoms_json) if intercoms_json else []

            async with async_session_maker() as session:
                result = await session.execute(
                    select(Intercom).options(selectinload(Intercom.entry))
                )
                intercom_objs = result.scalars().all()

            intercom_map = {
                ic.tech_name: intercom_to_dict(ic)
                for ic in intercom_objs
                if ic.tech_name
            }

            current_time_utc = datetime.now(timezone.utc)
            current_time = current_time_utc.astimezone(TIMEZONE)

            for intercom in current_intercoms:
                try:
                    last_update = datetime.fromisoformat(intercom["last_update"])

                    if last_update.tzinfo is None:
                        last_update = last_update.replace(tzinfo=timezone.utc)

                    delta = current_time - last_update
                    tech_name = intercom.get("tech_name")

                    merged_item = dict(intercom)
                    merged_item["intercom"] = intercom_map.get(tech_name)

                    if delta > timedelta(seconds=10):
                        print('Але')
                        await send_to_rabbitmq({
                            "event": "intercom_offline",
                            "tech_name": tech_name,
                            "timestamp": current_time.isoformat(),
                            "last_update": intercom["last_update"],
                            "intercom_data": merged_item,
                        }, QUEUE_OFF_INTERCOM)

                except Exception as inner_e:
                    print(f"intercom item error: {inner_e}")

        except OperationalError as db_err:
            print(f"DB reconnecting: {db_err}")
            await asyncio.sleep(1)
            continue

        except Exception as e:
            print(f"monitor_intercoms error: {e}")

        await asyncio.sleep(1*60*30)

async def cleanup_task():
    while True:
        delete_old_photos(days=1)
        await asyncio.sleep(60 * 60)