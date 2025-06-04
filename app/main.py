from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import router as api_router
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    app_name: str = "Productividad API"
    frontend_url: str

settings = Settings()
app = FastAPI(title=settings.app_name)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
