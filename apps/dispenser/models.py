from datetime import datetime

from sqlalchemy import Column, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from core.database import Base
from core.models import TimeStampMixin


class Dispenser(Base, TimeStampMixin):
    __tablename__ = "dispenser"
    id = Column(String(255), primary_key=True)
    flow_volume = Column(Float(precision=2))
    price = Column(Float(precision=2))
    status = Column(Boolean, default=False)


class DispenserEntries(Base, TimeStampMixin):
    __tablename__ = "dispenser_entries"
    id = Column(String(255), primary_key=True)

    open_time = Column(DateTime, nullable=False)
    close_time = Column(DateTime, nullable=True)

    dispenser_id = Column(ForeignKey("dispenser.id"), nullable=False)
    dispenser = relationship("Dispenser", cascade="delete")
