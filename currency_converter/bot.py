import asyncio
import re
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from config import BOT_TOKEN, CURRENCIES
from currency_converter import convert_currency
from keyboards import get_convert_keyboard, get_currency_keyboard

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

user_data = {}

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        f"Salom, {message.from_user.first_name}! 👋\n\n"
        "Men <b>Valyuta Konverteri Bot</b>man! 💱\n\n"
        "<b>Ikki usulda ishlaysiz:</b>\n\n"
        "1️⃣ <b>Tez usul:</b> Matn yuboring\n"
        "   Misol: <code>100 USD UZS</code>\n"
        "   Format: <code>summa qaysi_valyutadan qaysi_valyutaga</code>\n\n"
        "2️⃣ <b>Tugmalar orqali:</b> /convert buyrug'i\n\n"
        f"<b>Qo'llab-quvvatlanadigan valyutalar:</b>\n"
        f"{', '.join(CURRENCIES.keys())}",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text =="/convert")
async def convert_command(message: Message):
    user_id = message.from_user.id

    user_data[user_id] = {
        "from_currency": None,
        "to_currency": None,
        "amount": None
    }

    await message.answer(
        "💱 <b>Valyuta konvertatsiyasi</b>\n\n"
        "1️⃣ Qaysi valyutadan konvertatsiya qilmoqchisiz?",
        reply_markup=get_currency_keyboard("from"),
        parse_mode=ParseMode.HTML
    )

@dp.callback_query(F.data.startswith("from:"))
async def from_currency_selected(callback: CallbackQuery):
    user_id = callback.from_user.id

    currency = callback.data.split(":")[1]

    user_data[user_id]["from_currency"] = currency

    await callback.message.edit_text(
        f"✅ Tanlandi: <b>{CURRENCIES[currency]}</b>\n\n"
        "2️⃣ Qaysi valyutaga konvertatsiya qilasiz?",
        reply_markup=get_currency_keyboard("to"),
        parse_mode=ParseMode.HTML
    )

    await callback.answer()

@dp.callback_query(F.data.startswith("to:"))
async def to_currency_selected(callback: CallbackQuery):
    user_id = callback.from_user.id
    
    currency = callback.data.split(":")[1]
    
    user_data[user_id]["to_currency"] = currency
    
    from_curr = user_data[user_id]["from_currency"]
    
    await callback.message.edit_text(
        f"✅ <b>{CURRENCIES[from_curr]}</b> ➡️ <b>{CURRENCIES[currency]}</b>\n\n"
        f"3️⃣ Summani kiriting (faqat raqam):\n"
        f"Misol: <code>100</code>",
        parse_mode=ParseMode.HTML
    )
    
    await callback.answer()

@dp.callback_query(F.data.startswith("swap:"))
async def swap_currencies(callback: CallbackQuery):
    user_id = callback.from_user.id

    if user_id not in user_data:
        user_data[user_id] = {}

    parts = callback.data.split(":")
    from_curr = parts[1]
    to_curr = parts[2]

    user_data[user_id]["from_currency"] = to_curr
    user_data[user_id]["to_currency"] = from_curr

    await callback.message.edit_text(
        f"🔄 <b>O'zgartirildi!</b>\n\n"
        f"<b>{CURRENCIES[to_curr]}</b> ➡️ <b>{CURRENCIES[from_curr]}</b>\n\n"
        f"Summani kiriting:",
        parse_mode=ParseMode.HTML
    )

    await callback.answer("Valyutalar almashtirildi!")

@dp.callback_query(F.data == "restart")
async def restart_convert(callback: CallbackQuery):
    await convert_command(callback.message)
    await callback.answer()


@dp.message(F.text)
async def text_handler(message: Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id in user_data and user_data[user_id]["to_currency"] is not None:
        try:
            amount = float(text)

            from_curr = user_data[user_id]["from_currency"]
            to_curr = user_data[user_id]["to_currency"]

            wait_msg = await message.answer("💱 Hisoblanyapti...")
            result = await convert_currency(amount, from_curr, to_curr)

            if result is None:
                await wait_msg.edit_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
                return
            
            await wait_msg.edit_text(
                f"💰 <b>Konvertatsiya natijasi:</b>\n\n"
                f"<b>{amount:,.2f}</b> {from_curr} = <b>{result:,.2f}</b> {to_curr}\n\n"
                f"🇺🇸 {CURRENCIES[from_curr]}\n"
                f"➡️ {CURRENCIES[to_curr]}",
                reply_markup=get_convert_keyboard(from_curr, to_curr),
                parse_mode=ParseMode.HTML
            )

        except ValueError:
            await message.answer("❌ Iltimos, faqat raqam kiriting!\nMisol: <code>100</code>", parse_mode=ParseMode.HTML)

        return
    
    pattern = r"^(\d+\.?\d*)\s+([A-Z]{3})\s+([A-Z]{3})$"
    match = re.match(pattern, text.upper())

    if match:
        amount = float(match.group(1))
        from_curr = match.group(2)
        to_curr = match.group(3)

        if from_curr not in CURRENCIES or to_curr not in CURRENCIES:
            await message.answer(
                "❌ Noto'g'ri valyuta kodi!\n\n"
                f"Qo'llab-quvvatlanadigan: {', '.join(CURRENCIES.keys())}"
            )

            return
        
        wait_msg = await message.answer("💱 Hisoblanyapti...")

        result = await convert_currency(amount, from_curr, to_curr)

        if result is None:
            await wait_msg.edit_text("❌ Xatolik yuz berdi. Qaytadan urinib ko'ring.")
            return

        await wait_msg.edit_text(
            f"💰 <b>Konvertatsiya natijasi:</b>\n\n"
            f"<b>{amount:,.2f}</b> {from_curr} = <b>{result:,.2f}</b> {to_curr}\n\n"
            f"{CURRENCIES[from_curr]}\n"
            f"➡️ {CURRENCIES[to_curr]}",
            reply_markup=get_convert_keyboard(from_curr, to_curr),
            parse_mode=ParseMode.HTML
        )

    else:
        await message.answer(
            "❌ Noto'g'ri format!\n\n"
            "<b>To'g'ri format:</b>\n"
            "<code>summa qaysi_valyutadan qaysi_valyutaga</code>\n\n"
            "<b>Misol:</b>\n"
            "<code>100 USD UZS</code>\n"
            "<code>50 EUR RUB</code>\n\n"
            "Yoki /convert buyrug'ini ishlating.",
            parse_mode=ParseMode.HTML
        )

@dp.callback_query()
async def debug_callback(callback: CallbackQuery):
    print("Callback data:", callback.data)
    await callback.answer("Callback received!")

async def main():
    print("Valyuta convert boti ishga tushdi")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())