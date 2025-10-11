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
    section: Optional[str] = None
    price: Optional[float] = 0

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    section: Optional[str] = None 

class BookResponse(BookBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class CartItemBase(BaseModel):
    user_id: int
    book_id: int


class CartItemCreate(CartItemBase):
    pass


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    book: BookResponse  # relación anidada

    model_config = {"from_attributes": True}
