import aio_pika
import json
from src.config import get_config

conf = get_config()

RABBIT_URL = conf.rabbit.url

async def send_to_rabbitmq(message: dict, queue_name: str):
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