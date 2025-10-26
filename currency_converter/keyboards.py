from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import CURRENCIES

def get_currency_keyboard(action: str):
    keyboard = []

    row = []

    for code, name in CURRENCIES.items():
        button = InlineKeyboardButton(
            text=f"{name}",
            callback_data=f"{action}:{code}"
        )
        row.append(button)

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_convert_keyboard(from_curr: str, to_curr: str):
    keyboard = [
        InlineKeyboardButton(
            text="🔄 O'zgartirish",
            callback_data=f"swap:{from_curr}:{to_curr}"
        )
    ],
    [
        InlineKeyboardButton(
            text="🔁 Boshidan",
            callback_data="restart"
        )
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)