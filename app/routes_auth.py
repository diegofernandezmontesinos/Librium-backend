# app/routes_auth.py
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Dict
import os
import requests

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

# Config desde env (mejor colocar en .env en producción)
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Cloudflare Turnstile secret de env (opcional)
TURNSTILE_SECRET = os.getenv("TURNSTILE_SECRET", None)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(data: Dict[str, str], expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_captcha(token: str) -> bool:
    """
    Verifies Cloudflare Turnstile token.
    Returns True if successful, False otherwise.
    If TURNSTILE_SECRET is not set, returns True (so you can disable captcha in dev).
    """
    if not TURNSTILE_SECRET:
        # No secret configured -> skip verification (dev mode)
        return True

    try:
        resp = requests.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={"secret": TURNSTILE_SECRET, "response": token},
            timeout=5,
        )
        result = resp.json()
        return result.get("success", False)
    except requests.RequestException:
        return False


@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user with hashed password.
    """
    existing = db.query(models.User).filter(models.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Usuario ya existe")

    hashed_pw = get_password_hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    """
    Login endpoint:
    - Validates captchaToken (if configured)
    - Validates username/password
    - Returns 401/403 JSONResponse on error
    - On success sets an httpOnly cookie with the JWT
    """
    # 1) captcha (optional)
    if user.captchaToken is not None and not verify_captcha(user.captchaToken):
        return JSONResponse(status_code=403, content={"status": 403, "message": "Captcha inválido"})

    # 2) user lookup
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return JSONResponse(status_code=401, content={"status": 401, "message": "Credenciales inválidas"})

    # 3) create token
    access_token = create_access_token(
        data={"sub": db_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # 4) set cookie (httpOnly)
    response.set_cookie(
        key="autorizado",
        value=access_token,
        httponly=True,
        secure=False if os.getenv("DEV", "1") == "1" else True,
        samesite="Lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    return {"status": 200, "message": "Login successful", "username": db_user.username}


@router.get("/me")
def me(response: Response, db: Session = Depends(get_db)):
    """
    Simple 'me' endpoint: for demo purposes it only reports that the server is alive.
    In a real app, you would decode the JWT from the 'autorizado' cookie and fetch user info.
    """
    # NOTE: For real apps: validate the cookie JWT and fetch the user.
    return {"status": 200, "message": "ok"}
