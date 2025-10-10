# app/models.py
from sqlalchemy import Column, Integer, String, Text, Enum as SqlEnum
from .database import Base
import enum

class UserRole(enum.Enum):
    admin = "admin"
    user = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(SqlEnum(UserRole), default=UserRole.user, nullable=False)

class BookCategory(enum.Enum):
    TERROR = "terror"
    AUTHOR = "author"
    CLUB = "club"
    KIDS = "kids"
    NEW = "new"
    # añade más si hace falta

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)
    category = Column(SqlEnum(BookCategory), default=BookCategory.NEW, nullable=False)
