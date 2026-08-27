from app.schemas.common import APIResponse, ErrorDetail
from app.schemas.lead import (
    LeadCreate,
    LeadResponse,
    DemoBookRequest,
    DemoBookingResponse,
    AvailableSlotsResponse,
)
from app.schemas.roi import RoiCalculateRequest, RoiCalculateResponse
from app.schemas.contact import (
    ContactCreate,
    ContactResponse,
    NewsletterCreate,
    NewsletterResponse,
)

__all__ = [
    "APIResponse",
    "ErrorDetail",
    "LeadCreate",
    "LeadResponse",
    "DemoBookRequest",
    "DemoBookingResponse",
    "AvailableSlotsResponse",
    "RoiCalculateRequest",
    "RoiCalculateResponse",
    "ContactCreate",
    "ContactResponse",
    "NewsletterCreate",
    "NewsletterResponse",
]
