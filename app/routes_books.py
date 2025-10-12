from fastapi import (
    APIRouter, Depends, HTTPException, UploadFile, Form, Query
)
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
import math

from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/books", tags=["books"])

# 📂 Directorio de subida de imágenes
UPLOAD_DIR = "uploads/books"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 🌍 URL base de tu servidor (ajústala según tu entorno)
BASE_URL = "http://localhost:8000"


# -------------------------------
# 🟢 Crear libro
# -------------------------------
@router.post("/", response_model=schemas.BookResponse)
async def create_book(
    title: str = Form(...),
    author: str = Form(...),
    description: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    section: Optional[schemas.SectionEnum] = Form(None),
    price: float = Form(...),
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    """Crear un nuevo libro con validación y subida de imagen"""

    # 🚫 Verificar duplicado
    if db.query(models.Book).filter(models.Book.title == title).first():
        raise HTTPException(status_code=400, detail="Book already exists")

    # 🖼 Guardar imagen si se sube
    saved_image_url = None
    if image and image.filename:
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        saved_image_url = f"{BASE_URL}/{file_path}"

    # 🧱 Crear libro
    new_book = models.Book(
        title=title,
        author=author,
        description=description,
        year=year,
        section=section.value if section else None,
        price=price,
        image_url=saved_image_url,
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


# -------------------------------
# 🟡 Listar libros (con filtros y paginación)
# -------------------------------
@router.get("/", response_model=schemas.PaginatedBooks)
def list_books(
    section: Optional[schemas.SectionEnum] = Query(None),
    page: int = Query(1, ge=1),
    limit: int = Query(12, le=100),
    db: Session = Depends(get_db),
):
    """
    Listar todos los libros.
    Se puede filtrar por `section`, y paginar con `page` y `limit`.
    """
    query = db.query(models.Book)

    if section:
        query = query.filter(models.Book.section == section.value)

    total = query.count()
    books = (
        query.offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    # ✅ Normalizar URLs de imágenes
    for book in books:
        if book.image_url and not book.image_url.startswith("http"):
            book.image_url = f"{BASE_URL}/{book.image_url}"

    return {
        "items": books,
        "total": total,
        "page": page,
        "pages": math.ceil(total / limit),
        "limit": limit
    }


# -------------------------------
# 🟣 Actualizar libro
# -------------------------------
@router.put("/{book_id}", response_model=schemas.BookResponse)
async def update_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    description: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    section: Optional[schemas.SectionEnum] = Form(None),
    price: float = Form(...),
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db),
):
    """Actualizar los datos de un libro existente"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 📸 Subir nueva imagen si aplica
    if image and image.filename:
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_book.image_url = f"{BASE_URL}/{file_path}"

    # 🧩 Actualizar campos
    db_book.title = title
    db_book.author = author
    db_book.description = description
    db_book.year = year
    db_book.price = price
    db_book.section = section.value if section else None

    db.commit()
    db.refresh(db_book)
    return db_book


# -------------------------------
# 🔴 Eliminar libro
# -------------------------------
@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Eliminar un libro por su ID"""
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 🧹 Eliminar archivo físico si existe
    if db_book.image_url and os.path.exists(db_book.image_url.replace(BASE_URL + "/", "")):
        os.remove(db_book.image_url.replace(BASE_URL + "/", ""))

    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
