from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lead import Lead
from app.schemas.lead import LeadCreate
from app.core.security import normalize_email


async def create_or_update_lead(db: AsyncSession, lead_in: LeadCreate) -> Lead:
    """Create a new lead or update existing lead if email exists."""
    clean_email = normalize_email(lead_in.email)
    
    # Check if lead exists
    query = select(Lead).where(Lead.email == clean_email)
    result = await db.execute(query)
    existing_lead = result.scalars().first()

    if existing_lead:
        # Update existing lead details
        existing_lead.restaurant_name = lead_in.restaurant_name
        existing_lead.owner_name = lead_in.owner_name
        existing_lead.phone = lead_in.phone or existing_lead.phone
        existing_lead.tables_count = lead_in.tables_count
        existing_lead.city = lead_in.city or existing_lead.city
        existing_lead.source = lead_in.source
        await db.commit()
        await db.refresh(existing_lead)
        return existing_lead

    # Create new lead
    new_lead = Lead(
        restaurant_name=lead_in.restaurant_name,
        owner_name=lead_in.owner_name,
        email=clean_email,
        phone=lead_in.phone,
        tables_count=lead_in.tables_count,
        city=lead_in.city,
        source=lead_in.source,
        status="new",
    )
    db.add(new_lead)
    await db.commit()
    await db.refresh(new_lead)
    return new_lead
