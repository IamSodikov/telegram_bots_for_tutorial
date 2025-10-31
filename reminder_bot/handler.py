from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import re


scheduler = AsyncIOScheduler()

router = Router()

class Reminder(StatesGroup):
    reminder = State()
    reminder_time = State()

def timeout_calculate(user_msg: str) -> datetime | None:

    text = user_msg.lower()
    

    match = re.search(r'(\d+)\s*(soniya|daqiqa|soat|kun)', text)
    
    if match:
        num = int(match.group(1))
        time_unit = match.group(2)

        if time_unit in ["soniya", "sonia"]:
            return datetime.now() + timedelta(seconds=num)
        elif time_unit == "daqiqa":
            return datetime.now() + timedelta(minutes=num)
        elif time_unit == "soat":
            return datetime.now() + timedelta(hours=num)
        elif time_unit == "kun":
            return datetime.now() + timedelta(days=num)
    
    return None

async def send_reminder(chat_id: int, text: str, bot):
    
    await bot.send_message(chat_id, f"⏰ Eslatma: {text}")

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Salom eslatuvchi botga xush kelibsiz!!!\n"
        "/reminder buyrug'i bilan eslatma o'rnatishingiz mumkin!"
    )

@router.message(Command("reminder"))
async def reminder_handler(message: Message, state: FSMContext):
    await message.answer(
        "Eslatilishi kerak bo'lgan xabarni yozing.\n"
        "Misol: Turishim kerak!"
    )
    await state.set_state(Reminder.reminder)

@router.message(Reminder.reminder)
async def event_receive(message: Message, state: FSMContext):
    await state.update_data(reminder=message.text)
    await state.set_state(Reminder.reminder_time)
    await message.answer(
        "Vaqtni kiriting.\n"
        "Misol: 15 daqiqa keyin / 2 soat keyin / 1 kun keyin"
    )

@router.message(Reminder.reminder_time)
async def event_time(message: Message, state: FSMContext):

    reminder_time = timeout_calculate(message.text)
    
    if reminder_time is None:
        await message.answer(
            "❌ Vaqt formati noto'g'ri!\n"
            "To'g'ri misol: 15 daqiqa keyin"
        )
        return
    

    data = await state.get_data()
    reminder_text = data.get("reminder", "")
    
 
    scheduler.add_job(
        send_reminder,
        'date',
        run_date=reminder_time,
        args=[message.chat.id, reminder_text, message.bot]
    )
    
    await state.clear()
    
   
    time_diff = reminder_time - datetime.now()
    await message.answer(
        f"✅ Eslatma saqlandi!\n"
        f"📝 Xabar: {reminder_text}\n"
        f"⏰ Vaqt: {time_diff.seconds // 60} daqiqadan keyin"
    )