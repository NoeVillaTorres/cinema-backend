from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
#from sqlalchemy import select
from sqlalchemy.orm import Session

from auth import (
    create_access_token,
    get_current_user,
    verify_password,
)
from database import get_db
from models import User
from schemas import LoginRequest, TokenResponse, UserResponse


router = APIRouter(prefix="/auth", tags=["Auth"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, session: DbSession):
    email = data.email.strip().lower()

    user = session.scalar(
        select(User).where(User.email == data.email)
    )

    if user is None or not verify_password(
        data.password, user.password_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )

    return TokenResponse(
        access_token=create_access_token(user)
    )


@router.get("/me", response_model=UserResponse)
def get_me(
    user: Annotated[User, Depends(get_current_user)],
):
    return user