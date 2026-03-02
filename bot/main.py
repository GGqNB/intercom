import asyncio
import logging

from maxapi import Bot, Dispatcher
from config import MAX_TOKEN
from routers import router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=MAX_TOKEN)
dp = Dispatcher()

dp.include_routers(router)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())