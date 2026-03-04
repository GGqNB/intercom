import asyncio
import logging

from maxapi import Bot, Dispatcher
from config import MAX_TOKEN
from rabbit_consumer import rabbit_listener
from routers import router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=MAX_TOKEN)
dp = Dispatcher()

dp.include_routers(router)


async def main():
    await asyncio.gather(
        dp.start_polling(bot),
        rabbit_listener(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())