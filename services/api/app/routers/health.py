from fastapi import APIRouter
from app.core.db import db_check

router = APIRouter()

@router.get("")
def health():
    return {"status": "ok", "service": "api"}

@router.get("/db")
def health_db():
    ok = db_check()
    return {"status": "ok" if ok else "fail", "db": ok}