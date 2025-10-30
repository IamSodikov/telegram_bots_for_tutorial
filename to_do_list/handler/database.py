import aiosqlite
import os

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "tasks.db")


async def init_db():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE  IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL            
            )
        ''')
        await db.commit()

async def add_task(user_id: int, task_text: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO tasks (user_id, task) VALUES (?,?)",
            (user_id, task_text)
        )

        await db.commit()

    
async def get_tasks(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, task FROM tasks WHERE user_id = ?",
            (user_id,)
        )

        rows = await cursor.fetchall()
        return rows
    
async def delete_task(task_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        await db.commit()