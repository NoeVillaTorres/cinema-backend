from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TitleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    synopsis: str
    type: Literal["movie", "series"]
    release_year: int
    poster_url: str | None
    genres: list[str]

    @field_validator("genres", mode="before")
    @classmethod
    def serialize_genres(cls, value):
        return [
            genre if isinstance(genre, str) else genre.name
            for genre in value
        ]


class GenreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str