from app.database import Base, engine
from app import models  # importa i modelli definiti in models.py

def create_all_tables():
    print("Creazione delle tabelle nel database...")
    Base.metadata.create_all(bind=engine)
    print("Tabelle create con successo!")

if __name__ == "__main__":
    create_all_tables()