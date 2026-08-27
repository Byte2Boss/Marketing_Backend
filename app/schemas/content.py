from typing import List, Optional, Any, Dict
from pydantic import BaseModel, ConfigDict


# --- Pricing Schemas ---
class PricingTierResponse(BaseModel):
    id: str
    name: str
    tagline: str
    price_monthly: int
    price_annual: int
    is_popular: bool
    badge: Optional[str] = None
    tier_scope: str
    cta_text: str
    features: List[str]
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class PricingFeatureMatrixResponse(BaseModel):
    id: int
    feature: str
    starter: bool
    growth: bool
    enterprise: bool
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class PricingDataResponse(BaseModel):
    tiers: List[PricingTierResponse]
    matrix: List[PricingFeatureMatrixResponse]


# --- Testimonial Schemas ---
class TestimonialResponse(BaseModel):
    id: str
    author: str
    role: str
    restaurant: str
    quote: str
    metric: str
    avatar: str
    stars: int
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class TrustStatResponse(BaseModel):
    id: int
    value: str
    label: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class TestimonialsDataResponse(BaseModel):
    testimonials: List[TestimonialResponse]
    trust_stats: List[TrustStatResponse]


# --- FAQ Schemas ---
class FaqResponse(BaseModel):
    id: int
    category: str
    question: str
    answer: str
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class FaqsDataResponse(BaseModel):
    categories: List[str]
    faqs: List[FaqResponse]


# --- Feature Deep Dive Schemas ---
class FeatureDeepDiveResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    description: str
    category: str
    icon_name: str
    color: str
    metrics_badge: str
    bullet_points: List[str]
    display_order: int

    model_config = ConfigDict(from_attributes=True)


# --- Menu Concepts Schemas ---
class ConceptMenuItemResponse(BaseModel):
    id: int
    concept_id: str
    name: str
    price: int
    desc: str
    category: str
    upsell: Optional[Dict[str, Any]] = None
    display_order: int

    model_config = ConfigDict(from_attributes=True)


class MenuConceptResponse(BaseModel):
    id: str
    name: str
    concept: str
    accent_color: str
    vibe: str
    title: str
    tagline: str
    categories: List[str]
    display_order: int
    items: List[ConceptMenuItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
