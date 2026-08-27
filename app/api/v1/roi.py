from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_database, limiter
from app.schemas.roi import RoiCalculateRequest, RoiCalculateResponse
from app.schemas.common import APIResponse
from app.services.roi_service import calculate_and_save_roi

router = APIRouter(prefix="/roi", tags=["ROI Calculator Engine"])


@router.post("/calculate", response_model=APIResponse[RoiCalculateResponse])
@limiter.limit("30/minute")
async def calculate_roi(
    request: Request,
    roi_in: RoiCalculateRequest,
    db: AsyncSession = Depends(get_database),
):
    """
    Calculate dynamic restaurant revenue uplift, AI upselling gains, and labor savings.
    """
    result = await calculate_and_save_roi(db, roi_in)
    return APIResponse(
        success=True,
        data=result,
        message="ROI calculation computed successfully.",
    )
