from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from db import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(64), index=True, nullable=False)
    line_id = Column(Integer, index=True, nullable=True)
    product_id = Column(Integer, index=True, nullable=True)
    ts = Column(DateTime, index=True, nullable=False)


class Heartbeat(Base):
    __tablename__ = "heartbeats"

    device_id = Column(String(64), primary_key=True)
    fw_version = Column(String(32), nullable=False)
    last_seen = Column(DateTime, default=datetime.utcnow, nullable=False)
