from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.tenants import router as tenants_router
from app.routers.events import router as events_router
from app.routers.alerts import router as alerts_router

app = FastAPI(title="CloudGuard AI API", version="0.1.0")

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(tenants_router, prefix="/tenants", tags=["tenants"])
app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(alerts_router, prefix="/alerts", tags=["alerts"])