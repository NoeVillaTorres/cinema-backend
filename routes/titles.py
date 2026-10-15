from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from auth import require_admin
from database import get_db
from models import Genre, Title, User
from schemas import TitleCreate, TitleResponse, TitleUpdate


router = APIRouter(
    prefix="/titles",
    tags=["Titles"],
)

DbSession = Annotated[Session, Depends(get_db)]
AdminUser = Annotated[User, Depends(require_admin)]


# Funciones auxiliares

def find_title(session: Session, title_id: int) -> Title:
    statement = (
        select(Title)
        .options(selectinload(Title.genres))
        .where(Title.id == title_id)
    )

    title = session.scalar(statement)

    if title is None:
        raise HTTPException(
            status_code=404,
            detail="Título no encontrado",
        )

    return title


def find_genres(session: Session, genre_ids: list[int]) -> list[Genre]:
    if len(genre_ids) != len(set(genre_ids)):
        raise HTTPException(
            status_code=422,
            detail="No se permiten géneros duplicados",
        )

    genres = session.scalars(
        select(Genre).where(Genre.id.in_(genre_ids))
    ).all()

    if len(genres) != len(genre_ids):
        raise HTTPException(
            status_code=422,
            detail="Uno o más géneros no existen",
        )

    return genres


# Consultar catálogo

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


# Consultar título individual

@router.get("/{title_id}", response_model=TitleResponse)
def get_title(title_id: int, session: DbSession):
    return find_title(session, title_id)


# Crear título (solo administradores)

@router.post(
    "",
    response_model=TitleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_title(
    data: TitleCreate,
    session: DbSession,
    _admin: AdminUser,
):
    genres = find_genres(session, data.genre_ids)

    title = Title(
        **data.model_dump(exclude={"genre_ids"}),
        genres=genres,
    )

    session.add(title)
    session.commit()
    session.refresh(title, attribute_names=["genres"])

    return title


# Actualizar título (solo administradores)

@router.put("/{title_id}", response_model=TitleResponse)
def update_title(
    title_id: int,
    data: TitleUpdate,
    session: DbSession,
    _admin: AdminUser,
):
    title = find_title(session, title_id)
    genres = find_genres(session, data.genre_ids)

    for field, value in data.model_dump(
        exclude={"genre_ids"}
    ).items():
        setattr(title, field, value)

    title.genres = genres

    session.commit()
    session.refresh(title, attribute_names=["genres"])

    return title


# Eliminar título (solo administradores)

@router.delete(
    "/{title_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_title(
    title_id: int,
    session: DbSession,
    _admin: AdminUser,
):
    title = find_title(session, title_id)

    session.delete(title)
    session.commit()