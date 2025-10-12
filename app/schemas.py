from pydantic import BaseModel, HttpUrl
from typing import Optional, Union, List
from enum import Enum

# ==========================================================
# Enums
# ==========================================================

class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class SectionEnum(str, Enum):
    TOP_SELLER = "topSeller"
    FICTION = "fiction"
    KIDS = "kids"
    SPANISH_BOOKS = "spanishBooks"
    EBOOKS = "ebooks"
    OFFERTS = "offerts"
    TECHNICAL_BOOKS = "technicalBooks"
    TERROR = "terror"
    SCIENCE = "science"
    HISTORY = "history"
    AUTHOR = "author"
    CLUB = "club"
    NEW = "new"

# ==========================================================
# Users
# ==========================================================

class UserCreate(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.user  # por defecto "user"

class UserLogin(BaseModel):
    username: str
    password: str
    captchaToken: Optional[str] = None  # opcional

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole

    model_config = {"from_attributes": True}

# ==========================================================
# Books
# ==========================================================

class BookBase(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    year: Optional[int] = None
    image_url: Optional[Union[str, HttpUrl]] = None
    section: Optional[SectionEnum] = None  # 👈 ahora es tipado
    price: Optional[float] = 0

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None
    section: Optional[SectionEnum] = None  # 👈 tipado aquí también
    price: Optional[float] = None

class BookResponse(BookBase):
    id: int

    model_config = {"from_attributes": True}

# ==========================================================
# Cart Items
# ==========================================================

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

# ==========================================================
# Paginación de Libros
# ==========================================================

class PaginatedBooks(BaseModel):
    total: int
    page: int
    limit: int
    items: List[BookResponse]

