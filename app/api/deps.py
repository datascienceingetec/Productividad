import os
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..database import SessionLocal

API_KEY = os.getenv("API_KEY", "changeme")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_token(authorization: str = Header(default="")):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    token = authorization.split(" ")[1]
    if token != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid token")

