# app.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from db import Base, engine, get_db
from sqlalchemy.orm import Session
from schemas import EventIn, HeartbeatIn, MetricsOut
from crud import insert_events, metrics_last_minutes, recent_events,
upsert_heartbeat
from auth import require_token
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Contador de Unidades API")
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)
@app.get("/health")
def health():
return {"status": "ok"}
@app.post("/events")
def post_events(items: List[EventIn], db: Session = Depends(get_db), _: dict
= Depends(require_token)):
created = insert_events(db, items)
return {"inserted": created}
@app.post("/heartbeat")
def post_heartbeat(h: HeartbeatIn, db: Session = Depends(get_db)):
upsert_heartbeat(db, h.device_id, h.fw_version)
return {"status": "ok"}
@app.get("/metrics", response_model=MetricsOut)
def get_metrics(
line_id: Optional[int] = None,
product_id: Optional[int] = None,
minutes: int = 120,
db: Session = Depends(get_db),
_: dict = Depends(require_token)
):
total, series = metrics_last_minutes(db, line_id, product_id, minutes)
return {"total": total, "per_minute": series}
@app.get("/events/recent")
def get_recent_events(limit: int = 100, line_id: Optional[int] = None,
product_id: Optional[int] = None, db: Session = Depends(get_db), _: dict =
Depends(require_token)):
rows = recent_events(db, limit, line_id, product_id)
return [
{
"id": r.id,
"device_id": r.device_id,
"line_id": r.line_id,
"product_id": r.product_id,
"ts": r.ts
} for r in rows
]