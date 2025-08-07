from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId

# Импортируем наши модели и объект коллекции из соседних файлов
from app.models import UserModel, UserCreateModel, UserUpdateModel
from app.database import users_collection

# Создаем новый APIRouter. Это как "мини-приложение" FastAPI.
router = APIRouter()

@router.post("/", response_model=UserModel, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreateModel):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail=f"User with email '{user.email}' already exists")

    user_dict = user.model_dump()
    insert_result = users_collection.insert_one(user_dict)
    created_user = users_collection.find_one({"_id": insert_result.inserted_id})
    return created_user

@router.get("/", response_model=List[UserModel])
def list_users(limit: int = 10, skip: int = 0):
    users = list(users_collection.find().skip(skip).limit(limit))
    return users

@router.get("/{user_id}", response_model=UserModel)
def get_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail=f"Invalid user ID format: {user_id}")
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return user
    raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")

@router.put("/{user_id}", response_model=UserModel)
def update_user(user_id: str, user_data: UserUpdateModel):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail=f"Invalid user ID format: {user_id}")
    update_data = user_data.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail=f"Invalid user ID format: {user_id}")
    delete_result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
    return
