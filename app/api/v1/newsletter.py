from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_database, limiter
from app.models.newsletter import NewsletterSubscriber
from app.schemas.contact import NewsletterCreate, NewsletterResponse
from app.schemas.common import APIResponse
from app.core.security import normalize_email

router = APIRouter(prefix="/newsletter", tags=["Newsletter Engine"])


@router.post("/subscribe", response_model=APIResponse[NewsletterResponse], status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def subscribe_newsletter(
    request: Request,
    sub_in: NewsletterCreate,
    db: AsyncSession = Depends(get_database),
):
    """
    Subscribe an email address to product announcements & restaurant industry trends.
    """
    clean_email = normalize_email(sub_in.email)

    query = select(NewsletterSubscriber).where(NewsletterSubscriber.email == clean_email)
    result = await db.execute(query)
    existing_sub = result.scalars().first()

    if existing_sub:
        if not existing_sub.is_active:
            existing_sub.is_active = True
            await db.commit()
            await db.refresh(existing_sub)
        return APIResponse(
            success=True,
            data=NewsletterResponse.model_validate(existing_sub),
            message="You are already subscribed to the RestroMind AI newsletter!",
        )

    new_sub = NewsletterSubscriber(
        email=clean_email,
        source=sub_in.source,
        is_active=True,
    )
    db.add(new_sub)
    await db.commit()
    await db.refresh(new_sub)

    return APIResponse(
        success=True,
        data=NewsletterResponse.model_validate(new_sub),
        message="Thank you for subscribing to RestroMind AI insights!",
    )
