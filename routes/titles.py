from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import get_db
from models import Title, Genre
from schemas import TitleResponse


router = APIRouter(
    prefix="/titles",
    tags=["Titles"]
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("", response_model=list[TitleResponse])
def get_titles(
    session: DbSession,
    search: str | None = Query(default=None, max_length=100),
    type: Literal["movie", "series"] | None = None,
    genre: str | None = Query(default=None, max_length=100),
):
    statement = select(Title).options(
        selectinload(Title.genres)
    )

    if search:
        statement = statement.where(
            Title.name.ilike(f"%{search}%")
        )

    if type:
        statement = statement.where(
            Title.type == type
        )

    if genre:
        statement = statement.where(
            Title.genres.any(Genre.name == genre)
        )

    statement = statement.order_by(Title.name)

    return session.scalars(statement).all()