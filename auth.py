import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import User


load_dotenv()

SECRET_KEY = os.environ["JWT_SECRET_KEY"]
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

password_hash = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user: User) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user.id),
        "exp": expires_at,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme)
    ],
    session: Annotated[Session, Depends(get_db)],
) -> User:
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado o token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise error

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp"]},
        )

        user_id = int(payload["sub"])

    except (InvalidTokenError, ValueError, TypeError, KeyError):
        raise error

    user = session.get(User, user_id)

    if user is None:
        raise error

    return user


def require_admin(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )

    return user