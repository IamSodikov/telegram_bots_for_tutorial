import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")

CURRENCIES = {
    "USD": "🇺🇸 AQSh dollari",
    "EUR": "🇪🇺 Yevro",
    "RUB": "🇷🇺 Rossiya rubli",
    "UZS": "🇺🇿 O'zbek so'mi",
    "GBP": "🇬🇧 Ingliz funt sterlingi",
    "CNY": "🇨🇳 Xitoy yuani",
    "TRY": "🇹🇷 Turk lirasi",
    "KZT": "🇰🇿 Qozoq tengesi"
}