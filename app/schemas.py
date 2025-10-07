from pydantic import BaseModel, HttpUrl
from typing import Optional, Union
from enum import Enum

# Enum de roles
class UserRole(str, Enum):
    admin = "admin"
    user = "user"

# Usuarios
class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.user  # Por defecto es 'user'

class UserLogin(BaseModel):
    username: str
    password: str
    captchaToken: Optional[str] = None  # Opcional si no verificas captcha siempre

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole  # Enum

    model_config = {
        "from_attributes": True
    }

# Libros
class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    image_url: Optional[Union[str, HttpUrl]] = None 

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None

class BookResponse(BookBase):
    id: int

    model_config = {
        "from_attributes": True
    }
