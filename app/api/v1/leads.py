from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database, limiter
from app.schemas.lead import LeadCreate, LeadResponse
from app.schemas.common import APIResponse
from app.services.lead_service import create_or_update_lead

router = APIRouter(prefix="/leads", tags=["Leads & Trial Signups"])


@router.post("", response_model=APIResponse[LeadResponse], status_code=status.HTTP_201_CREATED)
@limiter.limit("20/minute")
async def register_lead(
    request: Request,
    lead_in: LeadCreate,
    db: AsyncSession = Depends(get_database),
):
    """
    Capture a new lead or 14-day free trial request from marketing CTAs.
    """
    lead = await create_or_update_lead(db, lead_in)
    lead_resp = LeadResponse.model_validate(lead)
    
    return APIResponse(
        success=True,
        data=lead_resp,
        message="Thank you! Your trial access request has been registered. Our onboarding specialist will reach out shortly.",
    )
