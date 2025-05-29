from datetime import date
from pydantic import BaseModel, Field

class ProductivityBase(BaseModel):
    email: str
    username: str
    cat: str
    division: str | None = None
    departamento: str | None = None
    productividad: float
    fecha: date

class ProductivityCreate(ProductivityBase):
    pass

class Productivity(ProductivityBase):
    id: int

    class Config:
        orm_mode = True
