import asyncio
import json
import aio_pika
import aiohttp
import aiofiles
from pathlib import Path
from config import RABBIT_URL, QUEUE_NAME, BACKEND_URL
from maxapi import Bot
from maxapi.types import InputMedia
import logging
import tempfile
from datetime import datetime
from keyboards import (
    open_door_kb
)
logger = logging.getLogger(__name__)

async def download_photo_to_file(url: str) -> Path:
    """Скачиваем фото во временный файл и возвращаем Path"""
    import aiohttp
    import tempfile

    tmp_dir = Path(tempfile.gettempdir())
    tmp_path = tmp_dir / f"tmp_photo_{asyncio.get_running_loop().time()}.jpg"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(tmp_path, "wb") as f:
                        f.write(await resp.read())
                    return tmp_path
                else:
                    raise Exception(f"HTTP {resp.status}")
    except Exception as e:
        logger.error(f"Ошибка скачивания фото: {e}")
        return None


async def rabbit_listener(bot: Bot):
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            try:
                payload = json.loads(message.body.decode())

                if not payload:
                    logger.warning("Пустой payload")
                    await message.reject(requeue=False)
                    continue

                users = payload.get("users", [])
                if not users:
                    logger.warning("Нет пользователей в payload")
                    await message.ack()
                    continue

                created_at_raw = payload.get("created_at")
                created_at_formatted = created_at_raw

                try:
                    dt = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
                    created_at_formatted = dt.strftime("%d.%m.%Y %H:%M:%S")
                except Exception:
                    pass

                text = (
                    f"📢 Новый вызов!\n\n"
                    f"🏠 Дом: {payload.get('house_id')}\n"
                    f"🏢 Квартира: {payload.get('flat')}\n"
                    f"🕒 Время: {created_at_formatted}"
                )

                photo_url = payload.get("photo_url")
                tmp_file_path = None

                if photo_url:
                    full_photo_url = f"{BACKEND_URL.rstrip('/')}/api/{photo_url.lstrip('/')}"
                    logger.info(f"PHOTO URL: {full_photo_url}")
                    tmp_file_path = await download_photo_to_file(full_photo_url)

                for user in users:
                    chat_id = user["chat_id"]

                    if tmp_file_path:
                        await bot.send_message(
                            chat_id=chat_id,
                            text=text,
                            attachments=[InputMedia(path=str(tmp_file_path))]
                        )

                        await bot.send_message(
                            chat_id=chat_id,
                            attachments=[open_door_kb()]
                        )
                    else:
                        await bot.send_message(
                            chat_id=chat_id,
                            text=text,
                            attachments=[open_door_kb()]
                        )

                if tmp_file_path and tmp_file_path.exists():
                    tmp_file_path.unlink()

                # ✅ подтверждаем сообщение
                await message.ack()

            except Exception as e:
                logger.error(f"Ошибка обработки сообщения из RabbitMQ: {e}")

                # ❌ не возвращаем сообщение обратно в очередь
                await message.reject(requeue=False)