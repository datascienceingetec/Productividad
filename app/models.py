from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class ProductivityRecord(Base):
    __tablename__ = "productivity"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    username = Column(String, nullable=False)
    cat = Column(String, nullable=False)
    division = Column(String, nullable=True)
    departamento = Column(String, nullable=True)
    productividad = Column(Float, nullable=False)
    fecha = Column(Date, nullable=False)
