from typing import List, Optional, Annotated
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId

# Pydantic v2 требует явного указания, как работать с типами вроде ObjectId.
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
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
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
