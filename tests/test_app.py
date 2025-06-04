import os
import sys
from datetime import date
import pytest

# Configure environment before importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['API_KEY'] = 'testtoken'

from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import crud, schemas
import importlib, sys
# Alias modules for relative imports used in endpoints
sys.modules['app.api.schemas'] = importlib.import_module('app.schemas')
sys.modules['app.api.crud'] = importlib.import_module('app.crud')
sys.modules['app.api.database'] = importlib.import_module('app.database')
sys.modules['app.api.v1.deps'] = importlib.import_module('app.api.deps')
from app.api.v1 import endpoints
from app.api.deps import verify_token
from fastapi import HTTPException

@pytest.fixture(autouse=True)
def setup_db():
    engine.dispose()
    try:
        os.remove('test.db')
    except OSError:
        pass
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()
    Base.metadata.drop_all(bind=engine)
    try:
        os.remove('test.db')
    except OSError:
        pass

def create_sample(db: Session, **kwargs):
    record = schemas.ProductivityCreate(
        email=kwargs.get('email', 'user@example.com'),
        username=kwargs.get('username', 'user'),
        cat=kwargs.get('cat', 'dev'),
        division=kwargs.get('division', 'div'),
        departamento=kwargs.get('departamento', 'dep'),
        productividad=kwargs.get('productividad', 1.0),
        fecha=kwargs.get('fecha', date.today()),
    )
    return crud.create_record(db, record)

def test_verify_token_valid():
    # Should not raise
    verify_token(authorization='Bearer testtoken')

def test_verify_token_invalid():
    with pytest.raises(HTTPException):
        verify_token(authorization='Bearer wrong')
    with pytest.raises(HTTPException):
        verify_token(authorization='Token testtoken')

def test_list_employees():
    db = SessionLocal()
    create_sample(db, email='a@example.com')
    create_sample(db, email='b@example.com')
    db.close()
    db2 = SessionLocal()
    result = endpoints.list_employees(db=db2)
    db2.close()
    assert set(result) == {'a@example.com', 'b@example.com'}

def test_employee_summary_found():
    db = SessionLocal()
    create_sample(db, email='c@example.com')
    db.close()
    db2 = SessionLocal()
    result = endpoints.employee_summary('c@example.com', db=db2)
    db2.close()
    assert len(result) == 1
    assert result[0].email == 'c@example.com'


def test_employee_summary_not_found():
    with pytest.raises(HTTPException):
        endpoints.employee_summary('missing@example.com', db=SessionLocal())

def test_metrics_filters():
    db = SessionLocal()
    create_sample(db, email='d@example.com', cat='cat1', fecha=date(2023,1,1))
    create_sample(db, email='d@example.com', cat='cat2', fecha=date(2023,1,2))
    db.close()
    db2 = SessionLocal()
    res1 = endpoints.metrics(email='d@example.com', db=db2)
    assert len(res1) == 2
    res2 = endpoints.metrics(categoria='cat1', db=db2)
    assert len(res2) == 1
    res3 = endpoints.metrics(fecha_inicio=date(2023,1,2), fecha_fin=date(2023,1,2), db=db2)
    assert len(res3) == 1
    db2.close()

def test_crud_functions_direct():
    db = SessionLocal()
    rec = create_sample(db, email='z@example.com', cat='catx')
    employees = crud.get_employees(db)
    assert rec.email in employees
    summary = crud.get_employee_summary(db, rec.email)
    assert len(summary) == 1
    metrics = crud.get_metrics(db, email=rec.email, categoria='catx')
    assert len(metrics) == 1
    db.close()
