from fastapi import FastAPI
from app import models, database
from app.routes_auth import router as auth_router

# Crear tablas
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
