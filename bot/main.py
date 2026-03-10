import asyncio
import logging
from maxapi.types import BotCommand
from maxapi import Bot, Dispatcher
from config import MAX_TOKEN
from rabbit_consumer import rabbit_listener
from routers import router

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
        rabbit_listener(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())