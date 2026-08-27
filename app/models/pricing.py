from sqlalchemy import Column, Integer, String, Boolean, JSON, Float
from app.core.database import Base


class PricingTier(Base):
    __tablename__ = "pricing_tiers"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    tagline = Column(String(255), nullable=False)
    price_monthly = Column(Integer, nullable=False)
    price_annual = Column(Integer, nullable=False)
    is_popular = Column(Boolean, default=False)
    badge = Column(String(50), nullable=True)
    tier_scope = Column(String(100), nullable=False)
    cta_text = Column(String(100), nullable=False)
    features = Column(JSON, nullable=False)  # List of strings
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class PricingFeatureMatrix(Base):
    __tablename__ = "pricing_matrix"

    id = Column(Integer, primary_key=True, autoincrement=True)
    feature = Column(String(255), nullable=False)
    starter = Column(Boolean, default=False)
    growth = Column(Boolean, default=True)
    enterprise = Column(Boolean, default=True)
    display_order = Column(Integer, default=0)
