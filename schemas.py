from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

class TitleCreate(BaseModel):
    @field_validator("name", "synopsis")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("El campo no puede estar vacío")

        return value

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    synopsis: str = Field(min_length=1)
    type: Literal["movie", "series"]
    release_year: int = Field(ge=1888, le=2100)
    poster_url: str | None = Field(default=None, max_length=500)
    genre_ids: list[int] = Field(min_length=1)


class TitleUpdate(TitleCreate):
    pass


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


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    role: Literal["admin", "user"]