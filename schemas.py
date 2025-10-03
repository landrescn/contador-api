from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class EventIn(BaseModel):
    device_id: str = Field(..., max_length=64)
    line_id: Optional[int] = None
    product_id: Optional[int] = None
    ts: datetime


class HeartbeatIn(BaseModel):
    device_id: str = Field(..., max_length=64)
    fw_version: str = Field(..., max_length=32)


class MetricsPoint(BaseModel):
    ts: datetime
    count: int


class MetricsOut(BaseModel):
    total: int
    per_minute: List[MetricsPoint]
