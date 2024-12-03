from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str

    class Config:
        env_file = ".env"

settings = Settings()

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client["students"]
