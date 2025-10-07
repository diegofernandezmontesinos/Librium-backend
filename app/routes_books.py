from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os, shutil

from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/books", tags=["books"])

UPLOAD_DIR = "uploads/books"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.BookResponse)
async def create_book(
    title: str = Form(...),
    author: str = Form(...),
    description: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    image_url: Optional[str] = Form(None),
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db)
):
    if db.query(models.Book).filter(models.Book.title == title).first():
        raise HTTPException(status_code=400, detail="Book already exists")

    saved_image_url = image_url
    if image:
        file_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        saved_image_url = file_path

    new_book = models.Book(
        title=title,
        author=author,
        description=description,
        year=year,
        image_url=saved_image_url,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/", response_model=List[schemas.BookResponse])
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@router.put("/{book_id}", response_model=schemas.BookResponse)
async def update_book(
    book_id: int,
    title: str = Form(...),
    author: str = Form(...),
    description: Optional[str] = Form(None),
    year: Optional[int] = Form(None),
    image_url: Optional[str] = Form(None),
    image: Optional[UploadFile] = None,
    db: Session = Depends(get_db)
):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # si sube nueva imagen
    if image:
        file_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_book.image_url = file_path
    elif image_url:
        db_book.image_url = image_url

    db_book.title = title
    db_book.author = author
    db_book.description = description
    db_book.year = year

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
