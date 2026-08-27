from sqlalchemy import Column, Integer, String, Boolean, Float, Text
from app.core.database import Base


class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(String(50), primary_key=True, index=True)
    author = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    restaurant = Column(String(150), nullable=False)
    quote = Column(Text, nullable=False)
    metric = Column(String(100), nullable=False)
    avatar = Column(String(500), nullable=False)
    stars = Column(Integer, default=5)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class TrustStat(Base):
    __tablename__ = "trust_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(50), nullable=False)
    label = Column(String(100), nullable=False)
    display_order = Column(Integer, default=0)
