from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class LeadBase(BaseModel):
    restaurant_name: str = Field(..., min_length=2, max_length=150, description="Name of the restaurant")
    owner_name: str = Field(..., min_length=2, max_length=100, description="Owner or manager full name")
    email: str = Field(..., pattern=EMAIL_REGEX, description="Business or personal email")
    phone: Optional[str] = Field(None, max_length=30, description="Phone number")
    tables_count: int = Field(10, ge=1, le=1000, description="Number of tables in restaurant")
    city: Optional[str] = Field(None, max_length=100, description="City / Region")
    source: str = Field("website_hero", max_length=50, description="Lead origin tag")


class LeadCreate(LeadBase):
    pass


class LeadResponse(LeadBase):
    id: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DemoBookRequest(BaseModel):
    restaurant_name: str = Field(..., min_length=2, max_length=150)
    owner_name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=EMAIL_REGEX)
    phone: Optional[str] = Field(None, max_length=30)
    tables_count: int = Field(15, ge=1, le=1000)
    city: Optional[str] = Field(None, max_length=100)
    preferred_date: str = Field(..., description="Selected demo date in YYYY-MM-DD format")
    time_slot: str = Field(..., description="Selected time slot like 10:00 AM")
    restaurant_type: str = Field("Fine Dining", max_length=50)
    notes: Optional[str] = Field(None, max_length=1000)


class DemoBookingResponse(BaseModel):
    booking_id: str
    lead_id: str
    restaurant_name: str
    owner_name: str
    email: str
    preferred_date: str
    time_slot: str
    restaurant_type: str
    confirmation_code: str
    status: str
    created_at: datetime


class AvailableSlotsResponse(BaseModel):
    date: str
    available_slots: List[str]
