from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TeamMemberBase(BaseModel):
    name: str
    role: str
    category: str
    bio: str
    avatar: str
    linkedin: Optional[str] = None
    github: Optional[str] = None
    display_order: int = 0
    is_active: bool = True


class TeamMemberCreate(TeamMemberBase):
    pass


class TeamMemberResponse(TeamMemberBase):
    id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
