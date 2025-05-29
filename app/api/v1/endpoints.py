from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import date
from app import schemas, crud
from app.database import Base, engine
from app.api.deps import get_db, verify_token
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/api/v1")


@router.get("/empleados", response_model=List[str])
def list_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)


@router.get("/empleado/{email}", response_model=List[schemas.Productivity])
def employee_summary(email: str, db: Session = Depends(get_db)):
    records = crud.get_employee_summary(db, email)
    if not records:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return records


@router.get("/metricas", response_model=List[schemas.Productivity])
def metrics(
    email: Optional[str] = None,
    categoria: Optional[str] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
):
    return crud.get_metrics(db, email=email, categoria=categoria, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

@router.post("/registrar-metrica", response_model=schemas.ProductivityCreate)
def register_metrics(
    record: schemas.ProductivityCreate,
    db: Session = Depends(get_db)
):
    return crud.create_record(db=db, record=record)

from typing import List

@router.post("/registrar-metricas")
def register_multiple_metrics(
    records: List[schemas.ProductivityCreate],
    db: Session = Depends(get_db)
):
    created = []
    for record in records:
        new_record = crud.create_record(db=db, record=record)
        created.append(new_record)
    return created
