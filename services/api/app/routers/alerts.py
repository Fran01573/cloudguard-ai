from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.session import get_db
from app.models import Alert, Event
from datetime import datetime, timedelta

router = APIRouter()

def score_event(event_type: str, severity: str, count_recent: int) -> int:
    base = 10
    if severity == "low":
        base = 25
    elif severity == "medium":
        base = 55
    elif severity == "high":
        base = 85

    # regla simple por tipo
    if event_type == "login_failed":
        base += 10

    # si hay muchos eventos recientes, sube riesgo
    base += min(20, count_recent * 3)

    return max(0, min(100, base))


@router.get("")
def list_alerts(db: Session = Depends(get_db)):
    alerts = db.query(Alert).order_by(desc(Alert.created_at)).limit(100).all()
    return alerts


@router.post("/from-events")
def create_alerts_from_events(tenant_id: str, minutes: int = 60, db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(minutes=minutes)

    events = (
        db.query(Event)
        .filter(Event.tenant_id == tenant_id)
        .filter(Event.created_at >= since)
        .order_by(desc(Event.created_at))
        .all()
    )

    created = []
    for ev in events:
        # cuenta eventos recientes del mismo tipo
        count_recent = (
            db.query(Event)
            .filter(Event.tenant_id == tenant_id)
            .filter(Event.event_type == ev.event_type)
            .filter(Event.created_at >= since)
            .count()
        )

        risk = score_event(ev.event_type, ev.severity, count_recent)

        alert = Alert(
            tenant_id=tenant_id,
            title=f"Detected: {ev.event_type} ({ev.severity})",
            risk_score=risk,
            status="open",
        )
        db.add(alert)
        created.append(alert)

    db.commit()

    # refrescar ids
    for a in created:
        db.refresh(a)

    return {"created": len(created), "alerts": created}