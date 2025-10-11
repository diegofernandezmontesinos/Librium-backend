# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

# Default local SQLite DB (dev). Puedes cambiarlo con la variable de entorno DATABASE_URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Para sqlite en file system, hay que pasar connect_args
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

# Crear engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa
Base = declarative_base()

def get_db() -> Generator:
    """Dependency que devuelve una sesión de DB y asegura que se cierre."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear todas las tablas definidas en modelos
# ⚠ Esto NO elimina datos existentes, pero no agrega columnas nuevas automáticamente en SQLite
from app import models  # importa tus modelos para que Base conozca las tablas
Base.metadata.create_all(bind=engine)
