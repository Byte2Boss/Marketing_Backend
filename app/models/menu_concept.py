from sqlalchemy import Column, Integer, String, Boolean, JSON, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class MenuConcept(Base):
    __tablename__ = "menu_concepts"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    concept = Column(String(150), nullable=False)
    accent_color = Column(String(20), nullable=False)
    vibe = Column(String(100), nullable=False)
    title = Column(String(150), nullable=False)
    tagline = Column(String(200), nullable=False)
    categories = Column(JSON, nullable=False)  # List of string category tabs
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    items = relationship("ConceptMenuItem", back_populates="concept", cascade="all, delete-orphan", lazy="selectin")


class ConceptMenuItem(Base):
    __tablename__ = "concept_menu_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    concept_id = Column(String(50), ForeignKey("menu_concepts.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    price = Column(Integer, nullable=False)  # In INR
    desc = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    upsell = Column(JSON, nullable=True)  # { message, suggestedItem: { name, price }, text }
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    concept = relationship("MenuConcept", back_populates="items")
