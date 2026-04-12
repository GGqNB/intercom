import asyncio
import json
import aio_pika
import aiohttp
import aiofiles
from pathlib import Path
from config import RABBIT_URL, QUEUE_NAME, BACKEND_URL, ADMIN_CHAT_ID
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


                
async def delete_after(bot: Bot, message_id: str, delay: int):
    """Удаляет сообщение через delay секунд"""
    await asyncio.sleep(delay)
    try:
        await bot.delete_message(message_id)
    except Exception as e:
        logger.warning(f"Не удалось удалить сообщение {message_id}: {e}")
        

async def consume_queue(queue_name: str, handler):
    connection = await aio_pika.connect_robust(RABBIT_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                try:
                    payload = json.loads(message.body.decode())
                    await handler(payload)
                except Exception as e:
                    logger.error(f"Queue {queue_name} error: {e}")
                    

async def handle_call(payload, bot: Bot):
    if not payload:
        return

    users = payload.get("users", [])
    if not users:
        return

    created_at_raw = payload.get("created_at")
    created_at_formatted = created_at_raw

    try:
        dt = datetime.fromisoformat(created_at_raw.replace("Z", "+00:00"))
        created_at_formatted = dt.strftime("%d.%m.%Y %H:%M:%S")
    except:
        pass

    text = (
        f"📢 Новый вызов!\n\n"
        f"🏠 Дом: {payload.get('house_id')}\n"
        f"🏢 Квартира: {payload.get('flat_number')}\n"
        f"🕒 Время: {created_at_formatted}"
    )

    photo_url = payload.get("photo_url")
    tmp_file_path = None

    if photo_url:
        full_photo_url = f"{BACKEND_URL.rstrip('/')}/api/{photo_url.lstrip('/')}"
        tmp_file_path = await download_photo_to_file(full_photo_url)

    for user in users:
        chat_id = user["chat_id"]
        open_token = payload.get("open_token", "")
        if tmp_file_path:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                attachments=[InputMedia(path=str(tmp_file_path))]
            )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=text,
                attachments=[open_door_kb()]
            )

    if tmp_file_path and tmp_file_path.exists():
        tmp_file_path.unlink()
        
    if open_token: 
        kb_message = await bot.send_message( 
                    chat_id=chat_id, 
                    text="Нажмите кнопку чтобы открыть дверь:",
                    attachments=[open_door_kb(open_token)]
                )

async def handle_intercom_crash(payload, bot: Bot):
    if payload.get("event") == "intercom_crash":
        tech_name = payload.get("tech_name")
        intercom_data = payload.get("intercom_data")

        text = (
            f"🚨 КРАШ ДОМОФОНА\n\n"
            f"🔧 Устройство: {tech_name}\n"
            f"🏠 Дом: {intercom_data.get('entry', {}).get('name') if intercom_data else 'unknown'}\n"
            f"📍 Адрес: {intercom_data.get('entry', {}).get('house_id') if intercom_data else 'unknown'}"
        )

        await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=text
            )
    elif payload.get("event") == "intercom_offline":
        tech_name = payload.get("tech_name")

        intercom_data = payload.get("intercom_data") or {}

        intercom = intercom_data.get("intercom") or {}
        entry = intercom.get("entry") or {}

        text = (
            f"🚨 СОН ДОМОФОНА\n\n"
            f"🔧 Устройство: {tech_name}\n"
            f"🏠 Дом: {entry.get('name', 'unknown')}\n"
            f"📍 Адрес: {entry.get('house_id', 'unknown')}"
        )

        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=text
        )
    else:
        return