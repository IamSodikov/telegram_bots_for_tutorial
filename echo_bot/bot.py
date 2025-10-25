import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\n"
        "Men Echo Bot'man. Menga yozgan xabaringizni qaytarib yuboraman."
    )

@dp.message()
async def echo_handler(message: Message):
    await message.answer(message.text)

async def main():
    print("Bot ishga tushdi bro!!!")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())