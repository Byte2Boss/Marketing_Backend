from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class ContactCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=EMAIL_REGEX)
    phone: Optional[str] = Field(None, max_length=30)
    subject: str = Field(..., min_length=2, max_length=150)
    message: str = Field(..., min_length=5, max_length=5000)


class ContactResponse(BaseModel):
    id: str
    full_name: str
    email: str
    subject: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NewsletterCreate(BaseModel):
    email: str = Field(..., pattern=EMAIL_REGEX)
    source: str = Field("footer", max_length=50)


class NewsletterResponse(BaseModel):
    id: str
    email: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
