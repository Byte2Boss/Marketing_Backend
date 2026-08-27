from sqlalchemy import Column, Integer, String, Boolean, JSON, Text
from app.core.database import Base


class FeatureDeepDive(Base):
    __tablename__ = "feature_deep_dives"

    id = Column(String(50), primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    subtitle = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    icon_name = Column(String(50), nullable=False)
    color = Column(String(20), nullable=False)
    metrics_badge = Column(String(100), nullable=False)
    bullet_points = Column(JSON, nullable=False)  # List of strings
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
