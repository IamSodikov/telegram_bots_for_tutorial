import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")