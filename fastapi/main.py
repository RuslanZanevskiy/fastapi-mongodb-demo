import os
from fastapi import FastAPI, HTTPException, status
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional, Annotated

# Используем более современные и точные инструменты из Pydantic v2
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

# --- Настройка FastAPI ---
app = FastAPI(
    title="FastAPI + MongoDB CRUD Example",
    description="Простое API для управления пользователями."
)

# --- Настройка MongoDB ---
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://root:example@localhost:27017/")
client = MongoClient(DATABASE_URL)
db = client["fastapidb"]
users_collection = db["users"]


# --- Модели данных Pydantic (версия 2.x) ---

# Pydantic v2 требует явного указания, как работать с типами вроде ObjectId.
# Мы создаем аннотацию `PyObjectId`, которая говорит Pydantic:
# 1. Проверять, что это валидный ObjectId.
# 2. Обрабатывать его как строку в JSON-схеме.
# `BeforeValidator(str)` гарантирует, что любое значение (включая ObjectId из базы)
# будет преобразовано в строку перед использованием.
PyObjectId = Annotated[str, BeforeValidator(str)]

# Модель для создания пользователя (то, что приходит в теле POST-запроса)
class UserCreateModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...) # EmailStr автоматически валидирует формат email

# Модель для обновления (то, что приходит в теле PUT-запроса)
class UserUpdateModel(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

# Модель для ответа (то, что API отдает наружу)
class UserModel(BaseModel):
    # Указываем Pydantic v2, как работать с моделью
    model_config = ConfigDict(
        populate_by_name=True, # Разрешает использовать alias (e.g., `_id` as `id`)
        arbitrary_types_allowed=True, # Разрешает типы вроде ObjectId
        json_schema_extra={ # Пример для документации /docs
            "example": {
                "id": "60d5ec49f7b4e2d3e1c9e8a1",
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
            }
        },
    )

    id: PyObjectId = Field(alias="_id")
    name: str
    email: EmailStr


# --- Эндпоинты API ---

@app.get("/", summary="Root Endpoint")
def root():
    return {"message": "FastAPI + MongoDB service is running"}

@app.post("/users/", response_model=UserModel, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateModel):
    """
    Создание нового пользователя.
    """
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail=f"User with email '{user.email}' already exists")

    user_dict = user.model_dump()
    insert_result = users_collection.insert_one(user_dict)
    created_user = users_collection.find_one({"_id": insert_result.inserted_id})
    return created_user

@app.get("/users/", response_model=List[UserModel])
def list_users(limit: int = 10, skip: int = 0):
    """
    Получение списка всех пользователей с пагинацией.
    """
    users = list(users_collection.find().skip(skip).limit(limit))
    return users

@app.get("/users/{user_id}", response_model=UserModel)
def get_user(user_id: str):
    """
    Получение одного пользователя по его ID.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail=f"Invalid user ID format: {user_id}")

    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user

    raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

@app.put("/users/{user_id}", response_model=UserModel)
def update_user(user_id: str, user_data: UserUpdateModel):
    """
    Обновление данных пользователя.
    Обновляются только переданные в теле запроса поля.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail=f"Invalid user ID format: {user_id}")

    # model_dump с exclude_unset=True создает dict только с теми полями, что были переданы
    update_data = user_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
    return updated_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    """
    Удаление пользователя по ID.
    """
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail=f"Invalid user ID format: {user_id}")

    delete_result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

    return # Возвращаем пустой ответ со статусом 204

@app.on_event("shutdown")
def shutdown_db_client():
    client.close()
