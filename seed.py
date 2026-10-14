from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from database import engine
from models import Title, Genre


# Géneros disponibles
GENRES = [
    "Acción",
    "Aventura",
    "Ciencia ficción",
    "Crimen",
    "Drama",
    "Fantasía",
    "Historia",
    "Misterio",
    "Suspenso",
    "Terror",
]


# Catálogo inicial
TITLES = [
    {
        "name": "Interstellar",
        "type": "movie",
        "release_year": 2014,
        "synopsis": "Un grupo de exploradores viaja más allá de nuestro sistema solar en busca de un nuevo hogar para la humanidad.",
        "poster_url": "/posters/interstellar.jpg",
        "genres": ["Ciencia ficción", "Drama"],
    },
    {
        "name": "The Dark Knight",
        "type": "movie",
        "release_year": 2008,
        "synopsis": "Batman enfrenta al Joker, un criminal que amenaza con sumir Gotham en el caos.",
        "poster_url": "/posters/the-dark-knight.jpg",
        "genres": ["Acción", "Drama"],
    },
    {
        "name": "Inception",
        "type": "movie",
        "release_year": 2010,
        "synopsis": "Un especialista en infiltrarse en sueños recibe la misión de implantar una idea en la mente de un empresario.",
        "poster_url": "/posters/inception.jpg",
        "genres": ["Ciencia ficción", "Acción"],
    },
    {
        "name": "The Matrix",
        "type": "movie",
        "release_year": 1999,
        "synopsis": "Un programador descubre que la realidad que conoce es una simulación controlada por máquinas.",
        "poster_url": "/posters/the-matrix.jpg",
        "genres": ["Ciencia ficción", "Acción"],
    },
    {
        "name": "Oppenheimer",
        "type": "movie",
        "release_year": 2023,
        "synopsis": "La historia del físico J. Robert Oppenheimer y su participación en el desarrollo de la primera bomba atómica.",
        "poster_url": "/posters/oppenheimer.jpg",
        "genres": ["Drama", "Historia"],
    },
    {
        "name": "Dune",
        "type": "movie",
        "release_year": 2021,
        "synopsis": "Paul Atreides llega al planeta Arrakis, donde su familia queda involucrada en una lucha por el control de un recurso extraordinario.",
        "poster_url": "/posters/dune.jpg",
        "genres": ["Ciencia ficción", "Aventura"],
    },
    {
        "name": "The Lord of the Rings: The Fellowship of the Ring",
        "type": "movie",
        "release_year": 2001,
        "synopsis": "Un joven hobbit emprende un viaje para destruir un anillo que amenaza con devolver el poder a un antiguo enemigo.",
        "poster_url": "/posters/the-lord-of-the-rings.jpg",
        "genres": ["Fantasía", "Aventura"],
    },
    {
        "name": "Parasite",
        "type": "movie",
        "release_year": 2019,
        "synopsis": "Dos familias de distintas clases sociales quedan vinculadas por una serie de engaños y acontecimientos inesperados.",
        "poster_url": "/posters/parasite.jpg",
        "genres": ["Drama", "Suspenso"],
    },
    {
        "name": "Breaking Bad",
        "type": "series",
        "release_year": 2008,
        "synopsis": "Un profesor de química comienza a fabricar metanfetaminas y termina involucrándose en el mundo del crimen.",
        "poster_url": "/posters/breaking-bad.jpg",
        "genres": ["Drama", "Crimen"],
    },
    {
        "name": "Dark",
        "type": "series",
        "release_year": 2017,
        "synopsis": "La desaparición de varios jóvenes revela secretos familiares y una misteriosa conexión entre diferentes épocas.",
        "poster_url": "/posters/dark.jpg",
        "genres": ["Ciencia ficción", "Misterio"],
    },
    {
        "name": "The Last of Us",
        "type": "series",
        "release_year": 2023,
        "synopsis": "Dos supervivientes atraviesan un territorio devastado por una infección que transformó el mundo.",
        "poster_url": "/posters/the-last-of-us.jpg",
        "genres": ["Drama", "Terror"],
    },
    {
        "name": "Stranger Things",
        "type": "series",
        "release_year": 2016,
        "synopsis": "Un grupo de amigos descubre experimentos secretos y fenómenos sobrenaturales en su pequeña ciudad.",
        "poster_url": "/posters/stranger-things.jpg",
        "genres": ["Ciencia ficción", "Misterio"],
    },
]


def seed_database():
    with Session(engine) as session:

        # Consultar géneros existentes
        existing_genres = {
            genre.name: genre
            for genre in session.scalars(select(Genre)).all()
        }

        # Crear géneros faltantes
        for name in GENRES:
            if name not in existing_genres:
                genre = Genre(name=name)
                session.add(genre)
                existing_genres[name] = genre

        session.flush()

        # Consultar títulos existentes junto con sus géneros
        existing_titles = {
            (title.name, title.type): title
            for title in session.scalars(
                select(Title).options(selectinload(Title.genres))
            ).all()
        }

        # Insertar o actualizar títulos
        for data in TITLES:
            key = (data["name"], data["type"])

            movie = existing_titles.get(key)

            if movie is None:
                movie = Title(
                    name=data["name"],
                    type=data["type"],
                    release_year=data["release_year"],
                    synopsis=data["synopsis"],
                    poster_url=data["poster_url"],
                )
                session.add(movie)
            else:
                movie.release_year = data["release_year"]
                movie.synopsis = data["synopsis"]
                movie.poster_url = data["poster_url"]

            movie.genres = [
                existing_genres[name]
                for name in data["genres"]
            ]

        session.commit()

    print("Catálogo inicial cargado correctamente.")


if __name__ == "__main__":
    seed_database()