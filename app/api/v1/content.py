from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_database
from app.schemas.common import APIResponse
from app.schemas.content import (
    PricingDataResponse,
    PricingTierResponse,
    PricingFeatureMatrixResponse,
    TestimonialsDataResponse,
    TestimonialResponse,
    TrustStatResponse,
    FaqsDataResponse,
    FaqResponse,
    FeatureDeepDiveResponse,
    MenuConceptResponse,
)
from app.models.pricing import PricingTier, PricingFeatureMatrix
from app.models.testimonial import Testimonial, TrustStat
from app.models.faq import Faq
from app.models.feature import FeatureDeepDive
from app.models.menu_concept import MenuConcept

router = APIRouter(prefix="/content", tags=["Dynamic Marketing Content"])


@router.get("/pricing", response_model=APIResponse[PricingDataResponse])
async def get_pricing_content(db: AsyncSession = Depends(get_database)):
    """Fetch pricing tiers and comparison matrix from PostgreSQL."""
    tiers_res = await db.execute(
        select(PricingTier).where(PricingTier.is_active == True).order_by(PricingTier.display_order.asc())
    )
    tiers = tiers_res.scalars().all()

    matrix_res = await db.execute(
        select(PricingFeatureMatrix).order_by(PricingFeatureMatrix.display_order.asc())
    )
    matrix = matrix_res.scalars().all()

    return APIResponse(
        success=True,
        data=PricingDataResponse(
            tiers=[PricingTierResponse.model_validate(t) for t in tiers],
            matrix=[PricingFeatureMatrixResponse.model_validate(m) for m in matrix],
        ),
        message="Pricing data retrieved successfully.",
    )


@router.get("/testimonials", response_model=APIResponse[TestimonialsDataResponse])
async def get_testimonials_content(db: AsyncSession = Depends(get_database)):
    """Fetch customer testimonials and trust stats from PostgreSQL."""
    test_res = await db.execute(
        select(Testimonial).where(Testimonial.is_active == True).order_by(Testimonial.display_order.asc())
    )
    testimonials = test_res.scalars().all()

    stats_res = await db.execute(
        select(TrustStat).order_by(TrustStat.display_order.asc())
    )
    trust_stats = stats_res.scalars().all()

    return APIResponse(
        success=True,
        data=TestimonialsDataResponse(
            testimonials=[TestimonialResponse.model_validate(t) for t in testimonials],
            trust_stats=[TrustStatResponse.model_validate(s) for s in trust_stats],
        ),
        message="Testimonials and trust stats retrieved successfully.",
    )


@router.get("/faqs", response_model=APIResponse[FaqsDataResponse])
async def get_faqs_content(db: AsyncSession = Depends(get_database)):
    """Fetch categorized FAQs from PostgreSQL."""
    faq_res = await db.execute(
        select(Faq).where(Faq.is_active == True).order_by(Faq.display_order.asc())
    )
    faqs = faq_res.scalars().all()

    # Extract distinct categories preserving order
    categories = []
    for f in faqs:
        if f.category not in categories:
            categories.append(f.category)

    return APIResponse(
        success=True,
        data=FaqsDataResponse(
            categories=categories,
            faqs=[FaqResponse.model_validate(f) for f in faqs],
        ),
        message="FAQs retrieved successfully.",
    )


@router.get("/features", response_model=APIResponse[List[FeatureDeepDiveResponse]])
async def get_features_content(db: AsyncSession = Depends(get_database)):
    """Fetch feature deep-dives from PostgreSQL."""
    feat_res = await db.execute(
        select(FeatureDeepDive).where(FeatureDeepDive.is_active == True).order_by(FeatureDeepDive.display_order.asc())
    )
    features = feat_res.scalars().all()

    return APIResponse(
        success=True,
        data=[FeatureDeepDiveResponse.model_validate(f) for f in features],
        message="Feature deep-dives retrieved successfully.",
    )


@router.get("/concepts", response_model=APIResponse[List[MenuConceptResponse]])
async def get_menu_concepts_content(db: AsyncSession = Depends(get_database)):
    """Fetch interactive simulator concepts and dishes from PostgreSQL."""
    concepts_res = await db.execute(
        select(MenuConcept).where(MenuConcept.is_active == True).order_by(MenuConcept.display_order.asc())
    )
    concepts = concepts_res.scalars().all()

    return APIResponse(
        success=True,
        data=[MenuConceptResponse.model_validate(c) for c in concepts],
        message="Menu concepts and items retrieved successfully.",
    )
