from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.session import get_db
from app.models import Tenant
from app.schemas import TenantCreate, TenantOut

router = APIRouter()

@router.post("", response_model=TenantOut)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):
    tenant = Tenant(name=payload.name)
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    return tenant

@router.get("", response_model=list[TenantOut])
def list_tenants(db: Session = Depends(get_db)):
    return db.query(Tenant).all()