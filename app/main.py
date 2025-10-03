from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

from app import models, database
from app.routes_auth import router as auth_router

# Crear tablas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Configuración CORS
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

# Logging de requests/responses
logger = logging.getLogger("uvicorn")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📩 Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 Response status: {response.status_code}")
    return response

# Incluir router de auth
app.include_router(auth_router, prefix="/auth", tags=["auth"])
