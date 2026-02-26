from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.session import get_db
from app.models import Event
from app.schemas import EventCreate, EventOut

router = APIRouter()

@router.post("", response_model=EventOut)
def create_event(payload: EventCreate, db: Session = Depends(get_db)):
    event = Event(
        tenant_id=payload.tenant_id,
        source=payload.source,
        event_type=payload.event_type,
        severity=payload.severity,
        raw=payload.raw,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("", response_model=list[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.created_at.desc()).limit(100).all()