from getpass import getpass

from sqlalchemy import select
from sqlalchemy.orm import Session

from auth import hash_password
from database import engine
from models import User


def main():
    email = input("Correo: ").strip().lower()

    if (
        not email
        or len(email) > 255
        or "@" not in email
        or email.startswith("@")
        or email.endswith("@")
    ):
        print("Introduce un correo electrónico válido.")
        return
    role = input("Rol (admin/user): ").strip().lower()

    if role not in ("admin", "user"):
        print("Rol inválido.")
        return

    password = getpass("Contraseña: ")
    confirmation = getpass("Confirmar contraseña: ")

    if len(password) < 8:
        print("La contraseña debe tener al menos 8 caracteres.")
        return

    if password != confirmation:
        print("Las contraseñas no coinciden.")
        return

    with Session(engine) as session:
        existing = session.scalar(
            select(User).where(User.email == email)
        )

        if existing:
            print("Ya existe un usuario con ese correo.")
            return

        user = User(
            email=email,
            password_hash=hash_password(password),
            role=role,
        )

        session.add(user)
        session.commit()

    print("Usuario creado correctamente.")


if __name__ == "__main__":
    main()