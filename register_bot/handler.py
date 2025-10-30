import asyncio
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import save_user_data, get_user_data

router = Router()

TIME_SLEEP = 10

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_age = State()
    waiting_for_phone = State()



async def timeout_clear(message: Message, state: FSMContext, expected_state):
    for i in range(TIME_SLEEP):
        await asyncio.sleep(1)
        current_state = await state.get_state()
        if current_state != expected_state:
            return
    await message.answer(
        "⏰ Siz belgilangan vaqt ichida javob yubormadingiz.\n"
        "Iltimos, /register buyrug‘i orqali qaytadan urinib ko‘ring."
    )
    await state.clear()

@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Salom! 👋 Anketa botga xush kelibsiz!\n"
        "Boshlash uchun /register buyrug‘ini yuboring."
    )


@router.message(Command("register"))
async def register_handler(message: Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Registration.waiting_for_name)
    asyncio.create_task(timeout_clear(message, state, Registration.waiting_for_name))


@router.message(Command("user_info"))
async def get_user_info_handler(message:Message):
    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    if user_data:
        await message.answer(
            f"🧾 Sizning ma'lumotlaringiz:\n\n"
            f"👤 Ism: {user_data['name']}\n"
            f"👨‍👩‍👧 Familiya: {user_data['surname']}\n"
            f"🎂 Yosh: {user_data['age']}\n"
            f"📞 Telefon: {user_data['phone']}"
        )
    else:
        await message.answer("Sizning ma'lumotlaringiz topilmadi. /register orqali ro‘yxatdan o‘ting.")


@router.message(Registration.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Familyangizni kiriting:")
    await state.set_state(Registration.waiting_for_surname)
    asyncio.create_task(timeout_clear(message, state, Registration.waiting_for_surname))


@router.message(Registration.waiting_for_surname)
async def get_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Yoshingizni kiriting:")
    await state.set_state(Registration.waiting_for_age)
    asyncio.create_task(timeout_clear(message, state, Registration.waiting_for_age))


@router.message(Registration.waiting_for_age)
async def get_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Iltimos, faqat son kiriting.")
        return
    await state.update_data(age=int(message.text))
    await message.answer("Telefon raqamingizni kiriting:")
    await state.set_state(Registration.waiting_for_phone)
    asyncio.create_task(timeout_clear(message, state, Registration.waiting_for_phone))


@router.message(Registration.waiting_for_phone)
async def get_phone(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_data["phone"] = message.text
    user_id = message.from_user.id

    save_user_data(user_id, user_data)

    await message.answer(
        f"✅ Ma'lumotlaringiz saqlandi!\n\n"
        f"Ism: {user_data['name']}\n"
        f"Familya: {user_data['surname']}\n"
        f"Yosh: {user_data['age']}\n"
        f"Telefon: {user_data['phone']}"
    )
    await state.clear()


