import asyncio
import logging
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher
from handler import router
from database import init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def main():
    init_db()

    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
