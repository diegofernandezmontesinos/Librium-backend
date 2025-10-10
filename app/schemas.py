# app/schemas.py (fragmentos)
from pydantic import BaseModel, HttpUrl
from typing import Optional, Union
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.user

class UserLogin(BaseModel):
    username: str
    password: str
    captchaToken: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    model_config = {"from_attributes": True}

# Libros
class BookCategory(str, Enum):
    TERROR = "terror"
    AUTHOR = "author"
    CLUB = "club"
    KIDS = "kids"
    NEW = "new"

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    image_url: Optional[Union[str, HttpUrl]] = None
    category: Optional[BookCategory] = BookCategory.NEW

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    model_config = {"from_attributes": True}
