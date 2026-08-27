import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, DateTime
from app.core.database import Base


class RoiCalculation(Base):
    __tablename__ = "roi_calculations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), nullable=True, index=True)
    restaurant_name = Column(String(150), nullable=True)
    tables_count = Column(Integer, nullable=False)
    avg_daily_orders = Column(Integer, nullable=False)
    avg_order_value = Column(Float, nullable=False)
    projected_monthly_gain = Column(Float, nullable=False)
    projected_hours_saved = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
