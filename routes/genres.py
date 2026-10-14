from fastapi import APIRouter
from sqlalchemy import select

from database import get_db
from schemas import GenreResponse
from models import Genre

from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[GenreResponse])
def get_genres(session: DbSession):
    statement = select(Genre).order_by(Genre.name)

    return session.scalars(statement).all()