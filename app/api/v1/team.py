from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_database
from app.models.team import TeamMember
from app.schemas.team import TeamMemberResponse
from app.schemas.common import APIResponse

router = APIRouter(prefix="/team", tags=["Team Members"])


@router.get("", response_model=APIResponse[List[TeamMemberResponse]])
async def list_team_members(db: AsyncSession = Depends(get_database)):
    """
    Fetch all active team members dynamically from the database.
    """
    query = select(TeamMember).where(TeamMember.is_active == True).order_by(TeamMember.display_order.asc())
    result = await db.execute(query)
    members = result.scalars().all()

    return APIResponse(
        success=True,
        data=[TeamMemberResponse.model_validate(m) for m in members],
        message="Team members retrieved successfully from database.",
    )
