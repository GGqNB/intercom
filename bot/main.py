import asyncio
import logging
from maxapi.types import BotCommand
from maxapi import Bot, Dispatcher
from config import MAX_TOKEN
from rabbit_consumer import consume_queue, handle_intercom_crash, handle_call
from routers import router
from config import QUEUE_NAME, QUEUE_OFFLINE
logging.basicConfig(level=logging.INFO)

bot = Bot(token=MAX_TOKEN)
async def setup_bot_commands():
    try:
        await bot.set_my_commands(
            BotCommand(name="start", description="Запуск бота или дом"),
            BotCommand(name="settings", description="Настройки"),
        )
    except Exception as e:
        logging.warning(f"Ошибка регистрации команд: {e}")
dp = Dispatcher()
dp.include_routers(router)


async def main():
    await setup_bot_commands(),
    await asyncio.gather(
        dp.start_polling(bot),
        consume_queue(QUEUE_NAME, lambda p: handle_call(p, bot)),
        consume_queue(QUEUE_OFFLINE, lambda p: handle_intercom_crash(p, bot)),
    )

if __name__ == "__main__":
    asyncio.run(main())