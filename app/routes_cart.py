# app/routes_cart.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("/{user_id}", response_model=List[schemas.CartItemResponse])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    cart_items = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == user_id)
        .all()
    )
    return cart_items


@router.post("/", response_model=schemas.CartItemResponse)
def add_to_cart(item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    # Verifica existencia del libro y usuario
    user = db.query(models.User).filter(models.User.id == item.user_id).first()
    book = db.query(models.Book).filter(models.Book.id == item.book_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not book:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    existing_item = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == item.user_id, models.CartItem.book_id == item.book_id)
        .first()
    )
    if existing_item:
        raise HTTPException(status_code=400, detail="El libro ya está en el carrito")

    cart_item = models.CartItem(user_id=item.user_id, book_id=item.book_id)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete("/{user_id}/remove/{book_id}")
def remove_from_cart(user_id: int, book_id: int, db: Session = Depends(get_db)):
    item = (
        db.query(models.CartItem)
        .filter(models.CartItem.user_id == user_id, models.CartItem.book_id == book_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado en el carrito")

    db.delete(item)
    db.commit()
    return {"message": "Libro eliminado del carrito"}


@router.delete("/{user_id}/clear")
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models.CartItem).filter(models.CartItem.user_id == user_id).delete()
    db.commit()
    return {"message": f"Carrito vaciado ({deleted} elementos eliminados)"}
