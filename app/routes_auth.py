from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import requests

from app import models, schemas, database

router = APIRouter()

# 🔑 Secret key para JWT
SECRET_KEY = "supersecretkey"  # Cámbialo por tu .env en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 🔑 Secret key de Cloudflare Turnstile
TURNSTILE_SECRET = "0x4AAAAAAB4m2ixb18GQb8pUtTqH9bNth1I"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_captcha(token: str) -> bool:
    """Valida el token del captcha en Cloudflare"""
    resp = requests.post(
        "https://challenges.cloudflare.com/turnstile/v0/siteverify",
        data={
            "secret": TURNSTILE_SECRET,
            "response": token
        }
    )
    result = resp.json()
    return result.get("success", False)

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    hashed_pw = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    # Usuario no encontrado o contraseña incorrecta
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return JSONResponse(
            status_code=401,
            content={"status": 401, "message": "Credenciales inválidas"}
        )

    # Aquí podrías agregar validación de captcha si quieres
    # if not verify_captcha(user.captchaToken):
    #     return JSONResponse(
    #         status_code=403,
    #         content={"status": 403, "message": "Captcha inválido"}
    #     )

    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # Set cookie HttpOnly
    response.set_cookie(
        key="autorizado",
        value=access_token,
        httponly=True,
        secure=False,  # True en producción con HTTPS
        samesite="Lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"status": 200, "message": "Login successful", "username": db_user.username}
