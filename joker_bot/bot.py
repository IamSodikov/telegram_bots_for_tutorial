import asyncio
import logging
import random
import json
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from config import BOT_TOKEN

logging.basicConfig(level = logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async  def start_handler(message: Message):
    await message.answer(
        "Joke botga hush kelibsiz!/n" 
        "/random buyrug'ini berishingiz bilan sizni ajoyib kulgu kutyapti"
    )

@dp.message(F.text.startswith("/random"))
async def random_joke_handler(message: Message):
    with open("data/jokes.json") as f:
        data = json.load(f)

    content = data["jokes"]
    item = random.choice(content)

    if item["type"] == "text":
        await message.answer(
            item["data"]
        )
    elif item["type"] == "image":
        photo = FSInputFile(item["data"])
        await message.answer_photo(
            photo
        )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())