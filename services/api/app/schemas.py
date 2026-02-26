from pydantic import BaseModel
from typing import Optional

class TenantCreate(BaseModel):
    name: str

class TenantOut(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True

class EventCreate(BaseModel):
    tenant_id: str
    source: Optional[str] = "simulator"
    event_type: str
    severity: Optional[str] = "low"
    raw: str

class EventOut(BaseModel):
    id: str
    tenant_id: str
    source: str
    event_type: str
    severity: str
    raw: str

    class Config:
        from_attributes = True