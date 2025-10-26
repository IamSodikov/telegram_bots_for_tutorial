import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import F
from aiogram.enums import ParseMode
from config import BOT_TOKEN, CHOICES
from game import get_bot_choice, determine_winner


logging.basicConfig(level=logging.INFO)


bot = Bot(BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(        
        "🎮 <b>Tosh-Qaychi-Qog'oz O'yini</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Assalomu alaykum, <b>{message.from_user.first_name}</b>! 👋\n\n"
        
        "📋 <b>O'yin qoidalari:</b>\n"
        "   🪨 Tosh → Qaychini yengadi\n"
        "   ✂️ Qaychi → Qog'ozni yengadi\n"
        "   📄 Qog'oz → Toshni yengadi\n\n"
        
        "🎯 <b>Qanday o'ynash:</b>\n"
        "O'yin boshlash uchun <code>/play</code> buyrug'ini yuboring!\n\n"
        
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "💡 <i>Omad tilayman!</i>",
        parse_mode="HTML"
    )


@dp.message(F.text == "/play")
async def play_handler(message: Message):
    button_rock = InlineKeyboardButton(
        text="🪨 Tosh",
        callback_data="choice:rock"
    )

    button_paper = InlineKeyboardButton(
        text="📄 Qog'oz",
        callback_data="choice:paper"
    )

    button_scissors = InlineKeyboardButton(
        text="✂️ Qaychi",
        callback_data="choice:scissors"
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [button_rock,button_paper,button_scissors]
        ]
    )

    await message.answer(
        "🎮 <b>Yangi O'yin!</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🤔 <b>Tanlovingizni qiling:</b>\n\n"
        "Quyidagi tugmalardan birini bosing 👇",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith("choice:"))
async def choice_handler(callback: CallbackQuery):
    user_choice = callback.data.split(":")[1]

    bot_choice = get_bot_choice()

    result = determine_winner(user_choice, bot_choice)

    if result == "win":
        result_text = "🎉 Siz yutdingiz!"
    elif result == "lose":
        result_text = "😔 Bot yutdi!"
    else: 
        result_text = "🤝 Durrang!"

    await callback.message.edit_text(
        f"{result} <b>O'yin Natijasi</b> {result}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{result_text}\n\n"
        f"👤 <b>Sizning tanlovingiz:</b>\n"
        f"     {CHOICES[user_choice]}\n\n"
        f"🤖 <b>Bot tanlovi:</b>\n"
        f"     {CHOICES[bot_choice]}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔄 Yana o'ynash: <code>/play</code>",
        parse_mode="HTML"
    )

    await callback.answer()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())