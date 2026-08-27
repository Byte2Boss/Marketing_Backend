from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lead import Lead, DemoBooking
from app.schemas.lead import DemoBookRequest, DemoBookingResponse
from app.core.security import generate_confirmation_code, normalize_email

DEFAULT_SLOTS = [
    "09:30 AM",
    "10:30 AM",
    "11:30 AM",
    "01:30 PM",
    "02:30 PM",
    "03:30 PM",
    "04:30 PM",
    "05:30 PM",
]


async def get_available_slots(db: AsyncSession, date_str: str) -> List[str]:
    """Retrieve available slots for a given date by subtracting already booked slots."""
    query = select(DemoBooking.time_slot).where(
        DemoBooking.preferred_date == date_str,
        DemoBooking.status.in_(["scheduled", "confirmed"]),
    )
    result = await db.execute(query)
    booked_slots = set(result.scalars().all())

    # Return slots that are not already booked
    available = [slot for slot in DEFAULT_SLOTS if slot not in booked_slots]
    return available if available else ["06:00 PM (Special Request)"]


async def book_demo(db: AsyncSession, request: DemoBookRequest) -> DemoBookingResponse:
    """Book a 15-minute live demo session and link or create a lead."""
    clean_email = normalize_email(request.email)

    # 1. Find or create lead
    lead_query = select(Lead).where(Lead.email == clean_email)
    result = await db.execute(lead_query)
    lead = result.scalars().first()

    if not lead:
        lead = Lead(
            restaurant_name=request.restaurant_name,
            owner_name=request.owner_name,
            email=clean_email,
            phone=request.phone,
            tables_count=request.tables_count,
            city=request.city,
            source="demo_booking_page",
            status="demo_scheduled",
        )
        db.add(lead)
        await db.flush()
    else:
        lead.restaurant_name = request.restaurant_name
        lead.owner_name = request.owner_name
        lead.status = "demo_scheduled"

    # 2. Create demo booking
    conf_code = generate_confirmation_code(prefix="RM")
    booking = DemoBooking(
        lead_id=lead.id,
        preferred_date=request.preferred_date,
        time_slot=request.time_slot,
        restaurant_type=request.restaurant_type,
        notes=request.notes,
        status="scheduled",
        confirmation_code=conf_code,
    )
    db.add(booking)
    await db.commit()
    await db.refresh(booking)

    return DemoBookingResponse(
        booking_id=booking.id,
        lead_id=lead.id,
        restaurant_name=lead.restaurant_name,
        owner_name=lead.owner_name,
        email=lead.email,
        preferred_date=booking.preferred_date,
        time_slot=booking.time_slot,
        restaurant_type=booking.restaurant_type,
        confirmation_code=booking.confirmation_code,
        status=booking.status,
        created_at=booking.created_at,
    )
