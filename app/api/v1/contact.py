from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database, limiter
from app.models.contact import ContactInquiry
from app.schemas.contact import ContactCreate, ContactResponse
from app.schemas.common import APIResponse
from app.core.security import normalize_email

router = APIRouter(prefix="/contact", tags=["Contact & Inquiries"])


@router.post("", response_model=APIResponse[ContactResponse], status_code=status.HTTP_201_CREATED)
@limiter.limit("15/minute")
async def submit_contact_inquiry(
    request: Request,
    inquiry_in: ContactCreate,
    db: AsyncSession = Depends(get_database),
):
    """
    Submit general inquiries, enterprise sales, or multi-unit franchise requests.
    """
    clean_email = normalize_email(inquiry_in.email)
    inquiry = ContactInquiry(
        full_name=inquiry_in.full_name,
        email=clean_email,
        phone=inquiry_in.phone,
        subject=inquiry_in.subject,
        message=inquiry_in.message,
    )
    db.add(inquiry)
    await db.commit()
    await db.refresh(inquiry)

    resp = ContactResponse.model_validate(inquiry)
    return APIResponse(
        success=True,
        data=resp,
        message="Thank you for reaching out! A RestroMind AI specialist will reply within 24 hours.",
    )
