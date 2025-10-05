# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app import models
from app.database import engine
from app.routes_auth import router as auth_router
from app.routes_books import router as books_router

# Crear tablas (si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="OnlineLibrary API")

# Configuración CORS (dev)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logger = logging.getLogger("uvicorn")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📩 Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 Response status: {response.status_code}")
    return response


# Rutas
app.include_router(auth_router)
app.include_router(books_router)
