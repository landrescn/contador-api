# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
class EventIn(BaseModel):
device_id: str = Field(..., max_length=64)
line_id: int
product_id: int
ts: datetime
class HeartbeatIn(BaseModel):
device_id: str
rssi: Optional[int] = None
pending: Optional[int] = None
uptime: Optional[int] = None
fw_version: Optional[str] = None
class MetricPoint(BaseModel):
ts: datetime
count: int
class MetricsOut(BaseModel):
total: int
per_minute: List[MetricPoint]