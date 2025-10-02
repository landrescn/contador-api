# crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, select
from datetime import datetime, timedelta
from models import Event, Device
from schemas import EventIn
DEDUP_WINDOW_SEC = 0.3 # tolerancia para duplicados
def insert_events(db: Session, items: list[EventIn]):
created = 0
for it in items:
# Dedup: existe evento mismo device y ts cercano?
q = db.query(Event).filter(
Event.device_id == it.device_id,
func.abs(func.extract('epoch', Event.ts) - func.extract('epoch',
it.ts)) <= DEDUP_WINDOW_SEC
)
if db.query(q.exists()).scalar():
continue
db.add(Event(
device_id=it.device_id,
line_id=it.line_id,
product_id=it.product_id,
ts=it.ts
))
created += 1
db.commit()
return created
def metrics_last_minutes(db: Session, line_id: int | None, product_id: int |
None, minutes: int = 120):
since = datetime.utcnow() - timedelta(minutes=minutes)
q = db.query(
func.date_trunc('minute', Event.ts).label('m'),
func.count(Event.id)
).filter(Event.ts >= since)
if line_id:
q = q.filter(Event.line_id == line_id)
if product_id:
q = q.filter(Event.product_id == product_id)
q = q.group_by('m').order_by('m')
rows = q.all()
total_q = db.query(func.count(Event.id)).filter(Event.ts >= since)
if line_id:
total_q = total_q.filter(Event.line_id == line_id)
if product_id:
total_q = total_q.filter(Event.product_id == product_id)
total = total_q.scalar() or 0
return total, [{"ts": r[0], "count": r[1]} for r in rows]
def recent_events(db: Session, limit: int = 100, line_id: int | None = None,
product_id: int | None = None):
q = db.query(Event).order_by(Event.ts.desc())
if line_id:
q = q.filter(Event.line_id == line_id)
if product_id:
q = q.filter(Event.product_id == product_id)
return q.limit(limit).all()
def upsert_heartbeat(db: Session, device_id: str, fw_version: str | None):
d = db.query(Device).get(device_id)
now = func.now()
if not d:
d = Device(id=device_id, fw_version=fw_version)
db.add(d)
d.last_seen = func.now()
if fw_version:
d.fw_version = fw_version
db.commit()