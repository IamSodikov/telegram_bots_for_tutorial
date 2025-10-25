import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from config import BOT_TOKEN
from questions import QUESTIONS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

user_data = {}

@dp.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id

    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        "Men Viktorina Bot'man. 🧠\n"
        "Sizga bir nechta savol beraman va javoblaringizni tekshiraman.\n\n"
        "Viktorinani boshlash uchun /quiz buyrug'ini yuboring!"
    )

@dp.message(Command("quiz"))
async def quiz_start(message: Message):
    user_id = message.from_user.id

    user_data[user_id]={
        "current_question": 0,
        "score":0
    }

    await send_question(message)

async def send_question(message: Message):
    user_id = message.from_user.id
    current_q = user_data[user_id]["current_question"]

    if current_q >= len(QUESTIONS):
        score = user_data[user_id]["score"]
        await message.answer(
            f"🎉 Viktorina tugadi!\n\n"
            f"Sizning natijangiz: {score}/{len(QUESTIONS)} to'g'ri javob!\n\n"
            f"Qaytadan boshlash uchun /quiz yuboring.",
            reply_markup=ReplyKeyboardRemove()
        )

    question_data = QUESTIONS[current_q]

    builder = ReplyKeyboardBuilder()

    for option in question_data["options"]:
        builder.add(KeyboardButton(text=option))

    builder.adjust(2)

    keyboard = builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )

    await message.answer(
        f"❓ Savol {current_q + 1}/{len(QUESTIONS)}:\n\n"
        f"{question_data['question']}",
        reply_markup=keyboard
    )

@dp.message()
async def check_answer(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.answer(
            "Viktorinani boshlash uchun /quiz buyrug'ini yuboring!"
        )
        return
    
    current_q = user_data[user_id]["current_question"]

    if current_q >= len(QUESTIONS):
        return
    
    question_data = QUESTIONS[current_q]
    
    user_answer = message.text

    if user_answer == question_data["correct"]:
        user_data[user_id]["score"] += 1
        await message.answer("✅ To'g'ri javob!")
    else:
        await message.answer(
            f"❌ Noto'g'ri! To'g'ri javob: {question_data['correct']}"
        )

    user_data[user_id]["current_question"] += 1

    await send_question(message)

async def main():
    print("Viktorina Bot ishga tushdi! ✅")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
