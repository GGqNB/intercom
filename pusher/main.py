import asyncio
import json
import aio_pika
import aiosmtplib
from email.mime.text import MIMEText
import os
import urllib.parse
from config import *
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Собираем RabbitMQ URL
vhost = RABBIT_VHOST or "/"
RABBIT_URL = f"amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:{RABBIT_PORT}/{urllib.parse.quote(vhost)}"
logging.info(f"RabbitMQ URL: {RABBIT_URL}")


async def send_email(subject: str, body: str):
    msg = MIMEText(body)
    msg["From"] = SMTP_USERNAME
    msg["To"] = EMAIL_TO
    msg["Subject"] = subject

    try:
        response = await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=SMTP_USERNAME,
            password=SMTP_PASSWORD,
        )

        code, message = response
        message_str = str(message).lower()

        if code in (250, 200) or "2.0.0 ok" in message_str or "ok" in message_str:
            logging.info(f"[OK] Email sent: {subject}")
            return True

        raise Exception(f"SMTP failed: {code} {message}")

    except Exception as e:
        logging.error(f"[ERROR] Email sending failed: {e}")
        raise


async def main():
    # Подключение к RabbitMQ с обработкой ошибок
    try:
        connection = await aio_pika.connect_robust(RABBIT_URL)
    except Exception as e:
        logging.error(f"[ERROR] RabbitMQ connection failed: {e}")
        return

    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        logging.info("Mail pusher worker started. Waiting for messages...")

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                try:
                    data = json.loads(message.body.decode())
                    tech_name = data.get("tech_name", "Unknown")

                    await send_email(
                        subject=f"Intercom offline: {tech_name}",
                        body=json.dumps(data, indent=2)
                    )

                    logging.info(f"[ACK] Message {message.delivery_tag} processed: {data}")
                    await message.ack()

                except Exception as e:
                    logging.error(f"[REQUEUE] Message {message.delivery_tag} failed: {e}")
                    await message.nack(requeue=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Worker stopped manually")
    except Exception as e:
        logging.error(f"Worker stopped due to error: {e}")