from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session

from models import Event, Heartbeat
from schemas import EventIn


def insert_events(db: Session, items: List[EventIn]) -> int:
    created = 0
    for it in items:
        db.add(
            Event(
                device_id=it.device_id,
                line_id=it.line_id,
                product_id=it.product_id,
                ts=it.ts,
            )
        )
        created += 1
    db.commit()
    return created


def upsert_heartbeat(db: Session, device_id: str, fw_version: str) -> None:
    hb = db.get(Heartbeat, device_id)
    if hb:
        hb.fw_version = fw_version
        hb.last_seen = datetime.utcnow()
    else:
        hb = Heartbeat(
            device_id=device_id,
            fw_version=fw_version,
            last_seen=datetime.utcnow(),
        )
        db.add(hb)
    db.commit()


def metrics_last_minutes(
    db: Session,
    line_id: Optional[int],
    product_id: Optional[int],
    minutes: int,
):
    since = datetime.utcnow() - timedelta(minutes=minutes)

    q = (
        select(
            func.date_trunc("minute", Event.ts).label("minute"),
            func.count().label("count"),
        )
        .where(Event.ts >= since)
        .group_by("minute")
        .order_by("minute")
    )

    if line_id is not None:
        q = q.where(Event.line_id == line_id)
    if product_id is not None:
        q = q.where(Event.product_id == product_id)

    rows = db.execute(q).all()
    total = sum(r.count for r in rows)
    series = [{"ts": r.minute, "count": r.count} for r in rows]
    return total, series


def recent_events(
    db: Session,
    limit: int = 100,
    line_id: Optional[int] = None,
    product_id: Optional[int] = None,
):
    q = select(Event).order_by(desc(Event.ts)).limit(limit)
    if line_id is not None:
        q = q.where(Event.line_id == line_id)
    if product_id is not None:
        q = q.where(Event.product_id == product_id)

    # db.execute devuelve tuplas (obj,), devolvemos solo el modelo
    return [row[0] for row in db.execute(q).all()]
