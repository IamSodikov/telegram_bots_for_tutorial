from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handler.database import add_task, get_tasks, delete_task

router = Router()

class ToDoList(StatesGroup):
    add_task = State()
    delet_task = State()

@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Salom todo botga xush kelibsiz!!!\n/add commandasi orqali yangi task qo'shishingiz mumkin")

@router.message(Command("add"))
async def add_task_handler(message: Message, state: FSMContext):
    await message.answer("Taskni matn ko'rinishida yozib yuboring: ")
    await state.set_state(ToDoList.add_task)

@router.message(ToDoList.add_task)
async def add_task_to_db(message: Message, state: FSMContext):
    user_id = message.from_user.id
    task_data =  message.text

    await add_task(user_id, task_data)

    await message.answer("Task ma'lumotlar omboriga qo'shildi!!!")

    await state.clear()

@router.message(Command("get_data"))
async def get_user_data(message: Message):
    user_id = message.from_user.id
    tasks_name = ""
    task_data = await get_tasks(user_id)

    for task in task_data:
        task_id = task[0]
        task_text = task[1]
        tasks_name += f"{task_id}. {task_text}\n"

    await message.answer(tasks_name)

@router.message(Command("delete"))
async def delete_task_handler(message: Message, state: FSMContext):
    await message.answer("Task id sini kiriting: ")
    await state.set_state(ToDoList.delet_task)

@router.message(ToDoList.delet_task)
async def delete_task_with_id(message: Message, state: FSMContext):
    await delete_task(message.text)
    await message.answer("Task o'chirildi")
    await state.clear()
