import os
from datetime import datetime
from typing import Any, Dict

from motor.motor_asyncio import AsyncIOMotorClient


class Mongo:
    _client = None

    @classmethod
    def client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            uri = os.getenv("MONGO_URI", "mongodb://mongo:27017")
            cls._client = AsyncIOMotorClient(uri)
        return cls._client
    
    @classmethod
    def db(cls):
        name = os.getenv("MONGO_DB", "weather_bot")
        return cls.client()[name]
    
    @classmethod
    async def save_weather_request(cls, city: str, payload: Dict[str, Any]) -> None:
        doc = {
            "city": city,
            "payload": payload,
            "ts": datetime.utcnow(),
        }
        await cls.db()["requests"].insert_one(doc)