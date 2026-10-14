# Importaciones
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Query
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import Literal


from database import engine
from models import Title, Genre

app = FastAPI(title="Cinema")


@app.get("/titles")
@app.get("/titles")
def get_titles(
    search: str | None = Query(default=None, max_length=100),
    type: Literal["movie", "series"] | None = None,
    genre: str | None = Query(default=None, max_length=100),
):
    with Session(engine) as session:
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

        titles = session.scalars(statement).all()

        return [
            {
                "id": title.id,
                "name": title.name,
                "synopsis": title.synopsis,
                "type": title.type,
                "release_year": title.release_year,
                "poster_url": title.poster_url,
                "genres": [genre.name for genre in title.genres],
            }
            for title in titles
        ]
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)