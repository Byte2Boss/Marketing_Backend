import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime
from app.core.database import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, default="Leadership")
    bio = Column(Text, nullable=False)
    avatar = Column(String(500), nullable=False)
    linkedin = Column(String(255), nullable=True)
    github = Column(String(255), nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
