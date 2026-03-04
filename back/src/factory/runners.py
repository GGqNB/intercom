from sqlalchemy.orm import selectinload
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

async def send_to_rabbitmq(message: dict, queue_name: str):
    try:
        connection = await aio_pika.connect_robust(RABBIT_URL)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(queue_name, durable=True)

            await channel.default_exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    content_type="application/json"
                ),
                routing_key=queue.name,
            )
    except Exception as e:
        print(f"Ошибка отправки в RabbitMQ: {e}")

async def monitor_intercoms():
    while True:
        try:
            intercoms_json = redis_client.get(conf.redis.INTERCOMS_KEY)
            current_intercoms = json.loads(intercoms_json) if intercoms_json else []

            query = select(Intercom).options(selectinload(Intercom.entry))
            async with async_session_maker() as session:
                result = await session.execute(query)
                intercom_objs: List[Intercom] = result.scalars().all()

          
            intercom_map: Dict[str, Dict[str, Any]] = {
                ic.tech_name: intercom_to_dict(ic) for ic in intercom_objs if ic.tech_name
            }

            current_time_utc = datetime.now(timezone.utc)
            current_time = current_time_utc.astimezone(TIMEZONE) 

            for intercom in current_intercoms:
                last_update = datetime.fromisoformat(intercom['last_update'])
                if last_update.tzinfo is None:
                    last_update = last_update.replace(tzinfo=timezone.utc)

                delta = current_time - last_update
                tech_name = intercom.get("tech_name")

                merged_item = dict(intercom)
                if tech_name and tech_name in intercom_map:
                    merged_item["intercom"] = intercom_map[tech_name]
                else:
                    merged_item["intercom"] = None

                if delta > timedelta(seconds=10):
                    # print(f"[{current_time.strftime('%H:%M:%S')}] Устарел домофон: {tech_name}")
                    await send_to_rabbitmq({
                        "event": "intercom_offline",
                        "tech_name": tech_name,
                        "timestamp": current_time.isoformat(),
                        "last_update": intercom["last_update"],
                        "intercom_data": merged_item,
                    }, QUEUE_OFF_INTERCOM)


        except Exception as e:
            print(f"[{current_time.strftime('%H:%M:%S')}] Ошибка в monitor_intercoms: {e}")

        await asyncio.sleep(1*60*60)

async def cleanup_task():
    while True:
        delete_old_photos(days=1)
        await asyncio.sleep(60 * 60)