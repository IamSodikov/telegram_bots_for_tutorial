import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import BOT_TOKEN
from handler import response_formatter, save_to_json, get_from_json

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class SearchState(StatesGroup):
    waiting_for_query = State()

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Salom botga xush kelibsiz /search kommandasi orqali lug'atdan so'zni qidirishingiz mumkin."
    )

@dp.message(F.text.startswith("/search"))
async def search_handler(message: Message, state: FSMContext):
    await message.answer(
        "Ingliz tilidagi so'zni yuboring: "
    )

    await state.set_state(SearchState.waiting_for_query)

@dp.message(SearchState.waiting_for_query)
async def search_state_handler(message: Message, state: FSMContext):
    word = message.text.strip().lower()

    search_from_json = await get_from_json(word)
    if search_from_json:
        await message.answer(search_from_json)
        await state.clear()
        return

    formatted_text = await response_formatter(word)
    if formatted_text:
        await save_to_json(word, formatted_text)
        await message.answer(formatted_text)
    else:
        await message.answer("Hech nima topilmadi")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())