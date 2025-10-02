# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index,
Boolean
from sqlalchemy.orm import relationship
from db import Base
class Line(Base):
__tablename__ = "lines"
id = Column(Integer, primary_key=True)
name = Column(String(100), unique=True, nullable=False)
status = Column(Boolean, default=True)
class Product(Base):
__tablename__ = "products"
id = Column(Integer, primary_key=True)
name = Column(String(120), unique=True, nullable=False)
sku = Column(String(60), unique=False)
status = Column(Boolean, default=True)
class Device(Base):
__tablename__ = "devices"
id = Column(String(64), primary_key=True) # device_id
line_id = Column(Integer, ForeignKey("lines.id"), nullable=True)
fw_version = Column(String(40))
last_seen = Column(DateTime)
line = relationship("Line")
class Event(Base):
__tablename__ = "events"
id = Column(Integer, primary_key=True)
device_id = Column(String(64), ForeignKey("devices.id"), nullable=False)
line_id = Column(Integer, ForeignKey("lines.id"), nullable=False)
product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
ts = Column(DateTime, nullable=False)
device = relationship("Device")
line = relationship("Line")
product = relationship("Product")
Index("idx_events_ts_line", Event.ts, Event.line_id)
class Shift(Base):
__tablename__ = "shifts"
id = Column(Integer, primary_key=True)
name = Column(String(50), nullable=False)
start_time = Column(String(8), nullable=False) # HH:MM:SS
end_time = Column(String(8), nullable=False)
days_mask = Column(String(14), nullable=True) # LMXJVSD flags