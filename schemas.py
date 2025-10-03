from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class EventIn(BaseModel):
    device_id: str = Field(..., max_length=64)
    line_id: Optional[int] = None
    product_id: Optional[int] = None
    ts: Optional[datetime] = None  # si no te llega, el backend puede definir por defecto


class HeartbeatIn(BaseModel):
    device_id: str = Field(..., max_length=64)
    fw_version: str = Field(..., max_length=64)


class PerMinuteItem(BaseModel):
    minute: str
    count: int


class MetricsOut(BaseModel):
    total: int
    per_minute: List[PerMinuteItem]
