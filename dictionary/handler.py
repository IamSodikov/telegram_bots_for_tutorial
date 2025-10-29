import aiohttp
import json 
import aiofiles
import os


async def  get_word_meaning(word: str = "hello"):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else: 
                return None
            

async def response_formatter(word: str):

    data = await get_word_meaning(word)

    if data is None:
        return None
    
    word_text = data[0]["word"]
    meaning = data[0]["meanings"][0]
    part_of_speech = meaning["partOfSpeech"]

    first_definition = meaning["definitions"][0]
    definition = first_definition["definition"]
    example = first_definition.get("example", "Misol mavjud emas")

    formatted_text = f"""📖 {word_text.title()}

🔹 {part_of_speech.title()}:
{definition}

Misol: {example}"""
    
    return formatted_text


async def save_to_json(word: str, formatted_text: str):

    
    file_path = "data/dictionary.json"

    if not os.path.exists("data"):
        os.makedirs("data")

    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content) if content.strip() else {}
    except FileNotFoundError:
        data = {}
    

    data[word.lower()] = formatted_text
    

    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))

    
async def get_from_json(word:str):
    file_path = "data/dictionary.json"

    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            content = await f.read()

            if not content.strip():
                return None
            data = json.loads(content)
            return data.get(word.lower())
    except FileNotFoundError:
        return None