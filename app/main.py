import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

from app.api.v1.endpoints import router as api_router

# Cargar variables de entorno
load_dotenv()

# Configurar conexión a la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Crear motor de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Crear sesión y base declarativa
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Crear la app
app = FastAPI(title="Productividad API")

# Incluir rutas
app.include_router(api_router)

# Crear DB y tablas si no existen
@app.on_event("startup")
def startup():
    if DATABASE_URL.startswith("sqlite"):
        db_path = DATABASE_URL.replace("sqlite:///", "")
        if not os.path.exists(db_path):
            print(f"⚙️  Creando base de datos en {db_path}...")
    Base.metadata.create_all(bind=engine)
