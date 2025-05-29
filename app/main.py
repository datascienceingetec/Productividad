from fastapi import FastAPI
from .api.v1.endpoints import router as api_router

app = FastAPI(title="Productividad API")

app.include_router(api_router)
