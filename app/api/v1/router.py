from fastapi import APIRouter
from app.api.v1.leads import router as leads_router
from app.api.v1.demo import router as demo_router
from app.api.v1.roi import router as roi_router
from app.api.v1.contact import router as contact_router
from app.api.v1.newsletter import router as newsletter_router
from app.api.v1.health import router as health_router

api_v1_router = APIRouter()

api_v1_router.include_router(leads_router)
api_v1_router.include_router(demo_router)
api_v1_router.include_router(roi_router)
api_v1_router.include_router(contact_router)
api_v1_router.include_router(newsletter_router)
api_v1_router.include_router(health_router)
