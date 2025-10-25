import aiohttp
from config import WEATHER_API_KEY

async def get_current_weather(city: str):
    url = "https://api.weatherapi.com/v1/current.json"

    params = {
        "q": city,
        "lang": "uz",
        "key": WEATHER_API_KEY
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {"success": True, "data": data}
                elif response.status == 404:
                    error_data = f"Quyidagicha xatolik mavjud: {response.status}"
                    return {"success": False, "data": error_data}
                else:
                    error_data = f"API xatosi: {response.status}"
                    return {"success": False, "error": "api_error", "status": response.status}
    except Exception as e:
        error_data = f"Xatolik yuz berdi: {e}"
        return {"success": False, "error": "unknown_error", "message": str(e) }

def format_weather(data):
    city = data["location"]["name"]
    country = data["location"]["country"]
    temp = data["current"]["temp_c"]
    feels_like = data["current"]["feelslike_c"]
    humidity = data["current"]["humidity"]
    description = data["current"]["condition"]["text"]
    wind_speed = data["current"]["wind_kph"]
    
    message = f"🌍 <b>{city}, {country}</b>\n\n"
    message += f"🌡 Harorat: <b>{temp}°C</b>\n"
    message += f"🤔 His qilinadi: {feels_like}°C\n"
    message += f"☁️ Holat: {description}\n"
    message += f"💧 Namlik: {humidity}%\n"
    message += f"💨 Shamol: {wind_speed} km/soat"
    
    return message