# app/routes_books.py (fragmentos)
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[schemas.BookResponse])
def list_books(
    db: Session = Depends(get_db),
    category: Optional[schemas.BookCategory] = Query(None),
    skip: int = 0,
    limit: int = 50,
):
    q = db.query(models.Book)
    if category:
        q = q.filter(models.Book.category == category)
    return q.offset(skip).limit(limit).all()

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
