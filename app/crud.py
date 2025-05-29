from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from typing import List, Optional
from datetime import date

# CRUD helper functions

def get_employees(db: Session) -> List[str]:
    return [email for (email,) in db.query(models.ProductivityRecord.email).distinct()] 


def get_employee_summary(db: Session, email: str):
    records = db.query(models.ProductivityRecord).filter(models.ProductivityRecord.email == email).all()
    return records


def get_metrics(
    db: Session,
    email: Optional[str] = None,
    categoria: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
):
    query = db.query(models.ProductivityRecord)
    if email:
        query = query.filter(models.ProductivityRecord.email == email)
    if categoria:
        query = query.filter(models.ProductivityRecord.cat == categoria)
    if fecha_inicio:
        query = query.filter(models.ProductivityRecord.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(models.ProductivityRecord.fecha <= fecha_fin)
    return query.all()


def create_record(db: Session, record: schemas.ProductivityCreate) -> models.ProductivityRecord:
    db_record = models.ProductivityRecord(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
