from fastapi import FastAPI
# Импортируем роутер пользователей и клиент БД
from .routes import users 
from .database import client

# --- Настройка FastAPI ---
app = FastAPI(
    title="FastAPI + MongoDB CRUD Example",
    description="Простое API для управления пользователями."
)

# Подключаем роутер с эндпоинтами для пользователей
# Все пути из users.py теперь будут доступны с префиксом /users
app.include_router(users.router, tags=["Users"], prefix="/users")

@app.get("/", tags=["Root"])
def root():
    return {"message": "FastAPI + MongoDB service is running"}

@app.on_event("shutdown")
def shutdown_db_client():
    client.close()
