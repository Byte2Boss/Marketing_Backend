from datetime import date
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database, limiter
from app.schemas.lead import DemoBookRequest, DemoBookingResponse, AvailableSlotsResponse
from app.schemas.common import APIResponse
from app.services.demo_service import get_available_slots, book_demo

router = APIRouter(prefix="/demo", tags=["Demo Booking Engine"])


@router.get("/available-slots", response_model=APIResponse[AvailableSlotsResponse])
async def list_available_slots(
    date_str: str = Query(..., alias="date", description="Date string in YYYY-MM-DD format"),
    db: AsyncSession = Depends(get_database),
):
    """
    Fetch open 15-minute live demo time slots for a given date.
    """
    slots = await get_available_slots(db, date_str)
    return APIResponse(
        success=True,
        data=AvailableSlotsResponse(date=date_str, available_slots=slots),
    )


@router.post("/book", response_model=APIResponse[DemoBookingResponse], status_code=status.HTTP_201_CREATED)
@limiter.limit("15/minute")
async def schedule_demo(
    request: Request,
    booking_in: DemoBookRequest,
    db: AsyncSession = Depends(get_database),
):
    """
    Schedule a 15-minute personalized RestroMind AI live demo walkthrough.
    """
    booking = await book_demo(db, booking_in)
    return APIResponse(
        success=True,
        data=booking,
        message=f"Live demo scheduled successfully! Your confirmation code is {booking.confirmation_code}.",
    )
