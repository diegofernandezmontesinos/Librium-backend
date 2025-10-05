# app/schemas.py
from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
    captchaToken: Optional[str] = None  # opcional si no siempre verificas captcha


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None


class BookResponse(BookBase):
    id: int

    class Config:
        from_attributes = True
