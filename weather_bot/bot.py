import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from weather import get_current_weather, format_weather


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        "Men Ob-havo Bot'man! 🌤️\n\n"
        "Menga shahar nomini yuboring va men sizga o'sha "
        "shahardagi ob-havo haqida ma'lumot beraman.\n\n"
        "<b>Misol:</b> <code>Tashkent</code>, <code>Moscow</code>, <code>London</code>",
        parse_mode=ParseMode.HTML
    )

@dp.message()
async def weather_handler(message: Message):
    city = message.text.strip()

    wait_msg = await message.answer("🔍 Ob-havo ma'lumotlarini qidiryapman...")

    result = await get_current_weather(city)

    if not result["success"]:
        await wait_msg.edit_text(
                f"❌ <b>{city}</b> shahri topilmadi!\n\n"
            "Iltimos, shahar nomini to'g'ri kiriting.\n"
            "Masalan: <code>Tashkent</code>",
            parse_mode=ParseMode.HTML
        )
        return

    weather_data = result["data"]
    weather_message = format_weather(weather_data)

    await wait_msg.edit_text(
        weather_message,
        parse_mode=ParseMode.HTML
    )

async def main():
    print("Ob havo bot ishga tushdi!!!")
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())

    
