import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    restaurant_name = Column(String(150), nullable=False)
    owner_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(30), nullable=True)
    tables_count = Column(Integer, nullable=False, default=10)
    city = Column(String(100), nullable=True)
    source = Column(String(50), nullable=False, default="website_hero")
    status = Column(String(30), nullable=False, default="new")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    demo_bookings = relationship("DemoBooking", back_populates="lead", cascade="all, delete-orphan")


class DemoBooking(Base):
    __tablename__ = "demo_bookings"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String(36), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False, index=True)
    preferred_date = Column(String(20), nullable=False)  # ISO YYYY-MM-DD
    time_slot = Column(String(20), nullable=False)        # e.g. "10:00 AM"
    restaurant_type = Column(String(50), nullable=False, default="Fine Dining")
    notes = Column(Text, nullable=True)
    status = Column(String(30), nullable=False, default="scheduled")
    confirmation_code = Column(String(20), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    lead = relationship("Lead", back_populates="demo_bookings")
