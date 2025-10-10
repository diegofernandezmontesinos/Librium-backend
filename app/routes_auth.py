# en app/routes_auth.py (reemplazar o añadir)
from fastapi import APIRouter, Depends, Response
from app.deps import get_current_user
from app.schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me", response_model=UserResponse)
def me(current_user = Depends(get_current_user)):
    """
    Devuelve datos del usuario autenticado basado en la cookie JWT.
    """
    return current_user

@router.post("/logout")
def logout(response: Response):
    # elimina cookie de sesión
    response.delete_cookie("autorizado")
    return {"status": 200, "message": "Logged out"}
