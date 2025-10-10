from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    Enum,  # 👈 Enum correcto
)
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import Enum
import enum


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False) 

    # relaciones
    cart_items = relationship("CartItem", back_populates="user")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, nullable=False)
    author = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)
    image_url = Column(String, nullable=True)

    # relaciones
    cart_items = relationship("CartItem", back_populates="book")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)

    user = relationship("User", back_populates="cart_items")
    book = relationship("Book", back_populates="cart_items")
