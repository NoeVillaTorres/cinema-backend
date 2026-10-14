from database import engine, Base
import models

def create_database():
    Base.metadata.create_all(bind=engine)
    print("Base de datos creada correctamente.")

if __name__ == "__main__":
    create_database()