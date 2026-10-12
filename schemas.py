
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=18, le=60)
    city: str = Field(..., min_length=1, max_length=100)
    is_active: bool = True

    @field_validator("name", "city")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value


class UserUpdate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=18, le=60)
    city: str = Field(..., min_length=1, max_length=100)
    is_active: bool

    @field_validator("name", "city")
    @classmethod
    def strip_required_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    city: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)