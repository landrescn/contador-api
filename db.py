# db.py
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables de entorno (.env en local o Environment en Render)
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # En Render debe estar configurada como Environment Variable
    raise RuntimeError("DATABASE_URL no está configurada")

# Motor de conexión y sesión
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos SQLAlchemy
Base = declarative_base()

# Dependencia para FastAPI: abre/cierra sesión por request
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
