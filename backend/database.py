import aiosqlite
import json
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "symptom_checker.db")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symptoms TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def save_query(symptoms: str, response: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO queries (symptoms, response, created_at) VALUES (?, ?, ?)",
            (symptoms, response, datetime.utcnow().isoformat()),
        )
        await db.commit()


async def get_history(limit: int = 20):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM queries ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
