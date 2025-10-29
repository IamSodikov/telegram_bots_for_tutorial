import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import BOT_TOKEN
from wikipedia_handler import search_wiki

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class SearchStates(StatesGroup):
    waiting_for_query = State()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"👋 Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "📚 Men <b>Wikipedia Bot</b>man va sizga kerakli ma'lumotlarni "
        "Wikipedia'dan topib berishga yordam beraman.\n\n"
        "🔍 <b>Qanday foydalanish kerak?</b>\n"
        "Shunchaki qidirmoqchi bo'lgan mavzungizni yuboring va men "
        "Wikipedia'dan eng mos natijalarni topib beraman.\n\n"
        "/search buyrug'ini yuboring matn kiritishdan avval"
        "💡 <b>Misol:</b>\n"
        "• O'zbekiston\n"
        "• Albert Einstein\n"
        "• Sun'iy intellekt\n\n"
        "❓ Yordam kerakmi? /help buyrug'ini yuboring.",
        parse_mode="HTML"
    )

@dp.message(F.text.startswith("/search"))
async def search_wiki_handler(message: Message, state: FSMContext):
    await message.answer(
        "Qidirmoqchi bo'lgan mavzuni yuboring: "
    )
    
    await state.set_state(SearchStates.waiting_for_query)

@dp.message(SearchStates.waiting_for_query)
async def search_state(message: Message, state: FSMContext):
    query = message.text

    loading = await message.answer("⏳ Qidiryapman...")

    result = await asyncio.to_thread(search_wiki, query)

    await loading.edit_text(result, parse_mode="HTML")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
