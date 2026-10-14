
# Importaciones
from sqlalchemy import (
    Table, Column, ForeignKey, CheckConstraint,
    String, Integer, Text
)

from sqlalchemy.orm import Mapped, mapped_column

from database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship

# Relación entre títulos y géneros
title_genres = Table(
    "title_genres",
    Base.metadata,
    Column(
        "title_id",
        ForeignKey("titles.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "genre_id",
        ForeignKey("genres.id", ondelete="CASCADE"),
        primary_key=True
    )
    
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(10), default="user", nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'user')",
            name="check_user_role"
        ),
    )

class Title(Base):
    __tablename__ = "titles"

    genres: Mapped[list["Genre"]] = relationship(
    secondary=title_genres,
    back_populates="titles"
)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    synopsis: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    type: Mapped[str] = mapped_column(
        String(10), nullable=False
    )
    release_year: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    poster_url: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "type IN ('movie', 'series')",
            name="check_title_type"
        ),
        CheckConstraint(
            "release_year BETWEEN 1888 AND 2100",
            name="check_release_year"
        ),
    )

class Genre(Base):
    __tablename__ = "genres"
    titles: Mapped[list["Title"]] = relationship(
    secondary=title_genres,
    back_populates="genres"
    )   

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )