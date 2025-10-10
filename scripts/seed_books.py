# scripts/seed_books.py
from app.database import SessionLocal, engine
from app import models
import os

models.Base.metadata.create_all(bind=engine)

books = [
    {"title": "It", "author": "Stephen King", "description": "Horror clásico", "year": 1986, "image_url": "https://picsum.photos/300/400?1", "category": models.BookCategory.TERROR},
    {"title": "El Resplandor", "author": "Stephen King", "description": "Hotel embrujado", "year": 1977, "image_url": "https://picsum.photos/300/400?2", "category": models.BookCategory.TERROR},
    {"title": "Cien años de soledad", "author": "G. García Márquez", "description": "Realismo mágico", "year": 1967, "image_url": "https://picsum.photos/300/400?3", "category": models.BookCategory.AUTHOR},
    {"title": "El Principito", "author": "Antoine de Saint-Exupéry", "description": "Clásico infantil", "year": 1943, "image_url": "https://picsum.photos/300/400?4", "category": models.BookCategory.KIDS},
    {"title": "Novedad 2025", "author": "Autor X", "description": "Libro del mes", "year": 2025, "image_url": "https://picsum.photos/300/400?5", "category": models.BookCategory.NEW},
    {"title": "Libro del club", "author": "Comité", "description": "Seleccionado para el club", "year": 2024, "image_url": "https://picsum.photos/300/400?6", "category": models.BookCategory.CLUB},
]

def run():
    db = SessionLocal()
    try:
        for b in books:
            exists = db.query(models.Book).filter(models.Book.title == b["title"]).first()
            if not exists:
                book = models.Book(**b)
                db.add(book)
        db.commit()
    finally:
        db.close()
    print("Seed complete")

if __name__ == "__main__":
    run()
