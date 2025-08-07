import os
from pymongo import MongoClient

# --- Настройка MongoDB ---
DATABASE_URL = os.getenv("DATABASE_URL")
client = MongoClient(DATABASE_URL)
db = client["fastapidb"]
users_collection = db["users"]
