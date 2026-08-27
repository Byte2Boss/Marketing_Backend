import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.pricing import PricingTier, PricingFeatureMatrix
from app.models.testimonial import Testimonial, TrustStat
from app.models.faq import Faq
from app.models.feature import FeatureDeepDive
from app.models.menu_concept import MenuConcept, ConceptMenuItem

logger = logging.getLogger(__name__)


async def seed_initial_content(session: AsyncSession):
    """Seed initial marketing data if tables are empty."""
    try:
        # 1. Seed Pricing Tiers
        existing_tier = await session.execute(select(PricingTier).limit(1))
        if not existing_tier.scalars().first():
            logger.info("Seeding initial pricing tiers...")
            tiers = [
                PricingTier(
                    id="starter",
                    name="Starter Setup",
                    tagline="Ideal for single boutique cafes, bakeries, and food trucks.",
                    price_monthly=1999,
                    price_annual=1499,
                    is_popular=False,
                    badge="Fast Setup",
                    tier_scope="Single Location",
                    cta_text="Start 14-Day Free Trial",
                    features=[
                        "Up to 15 Dine-In Tables",
                        "Dynamic Contactless QR Menus",
                        "Owner Web Dashboard & Item CRUD",
                        "Instant Out-of-Stock / 86 Toggling",
                        "High-Res Printable Table QRs (PNG)",
                        "Standard WhatsApp & Email Support",
                        "Basic Daily Analytics & Order Count",
                    ],
                    display_order=1,
                ),
                PricingTier(
                    id="growth",
                    name="Growth AI Tier",
                    tagline="Complete AI intelligence & kitchen sync for busy restaurants and bars.",
                    price_monthly=3999,
                    price_annual=2999,
                    is_popular=True,
                    badge="Most Popular",
                    tier_scope="Single or Dual Location",
                    cta_text="Claim 14-Day Free Trial",
                    features=[
                        "Up to 45 Dine-In Tables / Patio Stations",
                        "Autonomous AI Menu Engineering & Descriptions",
                        "Smart Upsell & Beverage Pairing Prompts (+24% AOV)",
                        "Real-Time Kitchen & Bar Ticket Dispatching",
                        "Category Scheduling (Breakfast, Lunch, Dinner)",
                        "Live Revenue Heatmaps & Peak Hour Insights",
                        "Direct UPI, Card & Digital Payment Processing",
                        "Priority 24/7 Phone & WhatsApp Support",
                    ],
                    display_order=2,
                ),
                PricingTier(
                    id="enterprise",
                    name="Enterprise Multi-Unit",
                    tagline="Tailored for restaurant chains, hospitality groups & franchises.",
                    price_monthly=7999,
                    price_annual=5999,
                    is_popular=False,
                    badge="Multi-Location",
                    tier_scope="3+ Outlets & Franchises",
                    cta_text="Talk to Enterprise Team",
                    features=[
                        "Unlimited Tables & Locations",
                        "Centralized Brand Menu Governance & Regional Pricing",
                        "Custom POS Integration (Petpooja, Posist, UrbanPiper)",
                        "Multi-Tenant Role-Based Access Control (RBAC)",
                        "Custom AI Training on Past Order Patterns",
                        "Dedicated Onboarding Engineer & Account Manager",
                        "99.99% Enterprise Uptime SLA Guarantee",
                        "Custom White-Label Branding & Domain Hosting",
                    ],
                    display_order=3,
                ),
            ]
            session.add_all(tiers)

        # 2. Seed Pricing Matrix
        existing_matrix = await session.execute(select(PricingFeatureMatrix).limit(1))
        if not existing_matrix.scalars().first():
            matrix_rows = [
                PricingFeatureMatrix(feature="Contactless QR Table Ordering", starter=True, growth=True, enterprise=True, display_order=1),
                PricingFeatureMatrix(feature="Real-Time 86 / Out-of-Stock Sync", starter=True, growth=True, enterprise=True, display_order=2),
                PricingFeatureMatrix(feature="Autonomous AI Pairing & Upsell Engine", starter=False, growth=True, enterprise=True, display_order=3),
                PricingFeatureMatrix(feature="Live Kitchen & Bar Ticket Routing", starter=False, growth=True, enterprise=True, display_order=4),
                PricingFeatureMatrix(feature="UPI & Payment Gateway Integration", starter=True, growth=True, enterprise=True, display_order=5),
                PricingFeatureMatrix(feature="Multi-Outlet Centralized Dashboard", starter=False, growth=False, enterprise=True, display_order=6),
                PricingFeatureMatrix(feature="Custom POS Sync (Petpooja, Posist)", starter=False, growth=False, enterprise=True, display_order=7),
                PricingFeatureMatrix(feature="Dedicated Account Manager & 24/7 SLA", starter=False, growth=False, enterprise=True, display_order=8),
            ]
            session.add_all(matrix_rows)

        # 3. Seed Testimonials & Trust Stats
        existing_test = await session.execute(select(Testimonial).limit(1))
        if not existing_test.scalars().first():
            testimonials = [
                Testimonial(
                    id="t1",
                    author="Chef Antoine Laurent",
                    role="Executive Chef & Owner",
                    restaurant="Le Bistro Botanique (Mumbai)",
                    quote="RestroMind AI increased our dessert and wine pairing sales by 26% in the very first month. Our servers spend less time taking routine drink reorders and more time delighting guests.",
                    metric="+26% Wine & Side Sales",
                    avatar="https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=500&auto=format&fit=crop&q=80",
                    stars=5,
                    display_order=1,
                ),
                Testimonial(
                    id="t2",
                    author="Sarah Jenkins",
                    role="General Manager",
                    restaurant="Copper Kettle Taproom (Bengaluru)",
                    quote="During packed Friday night rushes, our bar line used to be 4 deep. With RestroMind AI table QRs, patio guests order drinks right from their seats. Table turnover is 20 minutes faster!",
                    metric="-20 Min Table Turnaround",
                    avatar="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500&auto=format&fit=crop&q=80",
                    stars=5,
                    display_order=2,
                ),
                Testimonial(
                    id="t3",
                    author="Vikram Mehta",
                    role="Managing Partner",
                    restaurant="Saffron Spice Lounge (Ahmedabad)",
                    quote="We completely eliminated our ₹1,20,000 annual menu printing budget. Changing prices or marking a seafood special out-of-stock takes 2 seconds on my phone.",
                    metric="₹1,20,000 Annual Print Savings",
                    avatar="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=500&auto=format&fit=crop&q=80",
                    stars=5,
                    display_order=3,
                ),
            ]
            session.add_all(testimonials)

        existing_stats = await session.execute(select(TrustStat).limit(1))
        if not existing_stats.scalars().first():
            stats = [
                TrustStat(value="500+", label="Active Restaurant Venues", display_order=1),
                TrustStat(value="+24.8%", label="Average Order Value Lift", display_order=2),
                TrustStat(value="1.2M+", label="QR Orders Dispatched", display_order=3),
                TrustStat(value="99.99%", label="Platform Uptime SLA", display_order=4),
            ]
            session.add_all(stats)

        # 4. Seed FAQs
        existing_faqs = await session.execute(select(Faq).limit(1))
        if not existing_faqs.scalars().first():
            faqs = [
                Faq(category="General", question="Do my diners need to download an app from the App Store or Google Play?", answer="No! RestroMind AI is 100% web-based. Customers simply point their smartphone camera at the table QR code and the interactive digital menu opens instantly in their browser within 2 seconds.", display_order=1),
                Faq(category="Setup & Hardware", question="What hardware or equipment do I need to get started?", answer="None! You do not need expensive specialized POS terminals. You can manage your menu and view live incoming orders from any existing iPad, tablet, laptop, or smartphone.", display_order=2),
                Faq(category="AI & Menu", question="How does the AI Menu Engineering and Upselling work?", answer="Our AI model analyzes flavor pairings, beverage complements, and historical order combinations. When a diner selects an entree, the system intelligently suggests high-margin wine, appetizers, and sides that naturally pair with their dish.", display_order=3),
                Faq(category="Setup & Hardware", question="How fast can I update prices or mark sold-out items?", answer="Instantly! From your owner dashboard, toggling an item out-of-stock or updating a price reflects across all diner tables in under 2 seconds with zero page refresh required.", display_order=4),
                Faq(category="Pricing & Billing", question="Is there a free trial or long-term contract?", answer="We offer a 14-day full-access free trial with zero upfront credit card required. All standard plans are month-to-month with no cancellation penalties, or you can choose annual billing for a discount.", display_order=5),
                Faq(category="Pricing & Billing", question="Do you support multi-location restaurant chains or franchises?", answer="Yes! Our Enterprise tier provides centralized multi-location menu governance, regional pricing overrides, and corporate analytics across all franchise branches.", display_order=6),
            ]
            session.add_all(faqs)

        # 5. Seed Feature Deep Dives
        existing_feats = await session.execute(select(FeatureDeepDive).limit(1))
        if not existing_feats.scalars().first():
            features = [
                FeatureDeepDive(
                    id="dynamic-qr",
                    title="Instant Digital QR Menus",
                    subtitle="Sub-2-second browser loads with zero app installs required.",
                    description="Guests scan an elegant acrylic table QR stand and are immediately greeted with a rich, photo-forward menu tailored to their specific table station.",
                    category="Guest Experience",
                    icon_name="QrCode",
                    color="#10b981",
                    metrics_badge="3-Sec Scan to Table",
                    bullet_points=[
                        "Dynamic table-specific deep linking (Patio, Table 04, VIP Booth)",
                        "Crisp retina-ready dish imagery with dietary/allergen tags",
                        "Multi-language support for international tourist guests",
                        "Sub-200ms load time even on congested 4G cellular networks",
                    ],
                    display_order=1,
                ),
                FeatureDeepDive(
                    id="ai-upsell",
                    title="Autonomous AI Upsell Engine",
                    subtitle="Turn every digital menu into an award-winning sommelier.",
                    description="Our contextual recommendation engine analyzes flavor profiles, past order patterns, and inventory margins to suggest high-converting drink pairings and desserts in real time.",
                    category="Revenue Optimization",
                    icon_name="Sparkles",
                    color="#6366f1",
                    metrics_badge="+24.8% Average Ticket Size",
                    bullet_points=[
                        "Automatic wine, craft beer, and side pairing recommendations",
                        "High-margin item prioritization based on kitchen surplus",
                        "Dynamic basket bundle deals (Entree + Beverage combos)",
                        "A/B tested prompt triggers with 34% average conversion take rate",
                    ],
                    display_order=2,
                ),
                FeatureDeepDive(
                    id="kitchen-kds",
                    title="Real-Time Kitchen Display Sync",
                    subtitle="Eliminate waiter handwriting errors and speed up food prep.",
                    description="Orders placed by guests route instantaneously to kitchen prep screens and bar displays with item notes and table numbers.",
                    category="Kitchen Operations",
                    icon_name="Zap",
                    color="#f59e0b",
                    metrics_badge="-18 Min Fast Table Turn",
                    bullet_points=[
                        "Sub-second order dispatching to kitchen stations",
                        "Cooking time tracking with prep timers and alert thresholds",
                        "Bar and kitchen station segregation for beverage tickets",
                        "Direct runner notifications when orders are marked ready",
                    ],
                    display_order=3,
                ),
                FeatureDeepDive(
                    id="stock-sync",
                    title="2-Second Live 86 & Price Control",
                    subtitle="Update prices and 86 items across all tables in real time.",
                    description="Sold out of your fresh sea bass special? Tap '86' on your phone and every active diner table reflects the change in 2 seconds with zero page reloads.",
                    category="Menu Management",
                    icon_name="CheckCircle2",
                    color="#ef4444",
                    metrics_badge="₹0 Reprint Waste",
                    bullet_points=[
                        "One-click out-of-stock toggling from any mobile browser",
                        "Dynamic happy hour and lunch/dinner automated schedule shifts",
                        "Instant pricing adjustments across single or multi-unit outlets",
                        "Complete elimination of costly paper menu reprinting",
                    ],
                    display_order=4,
                ),
            ]
            session.add_all(features)

        # 6. Seed Menu Concepts
        existing_concepts = await session.execute(select(MenuConcept).limit(1))
        if not existing_concepts.scalars().first():
            c1 = MenuConcept(
                id="cafe",
                name="Artisan Cafe & Roastery",
                concept="Specialty Coffee, Sourdough & Brunch",
                accent_color="#10b981",
                vibe="Cozy Morning Glow",
                title="Morning Bloom Cafe",
                tagline="Table #04 • Digital Dine-In",
                categories=["All", "Espresso & Brews", "Brunch & Bakery", "Artisan Toasts"],
                display_order=1,
            )
            session.add(c1)
            await session.flush()

            session.add_all([
                ConceptMenuItem(concept_id="cafe", name="Single Origin Flat White", price=240, desc="Velvety micro-foam with Ethiopian heirloom beans.", category="Espresso & Brews", upsell={"message": "⭐ Sommelier AI: Fresh butter croissants just came out of the oven!", "suggestedItem": {"name": "Almond Flaked Croissant", "price": 180}, "text": "Pairs wonderfully with our warm, freshly baked Butter Croissant (+ ₹180)"}, display_order=1),
                ConceptMenuItem(concept_id="cafe", name="Avocado Sourdough Tartine", price=380, desc="Hass avocado, pickled shallots, dukkah crumble.", category="Artisan Toasts", upsell={"message": "⭐ Boost your brunch with a fresh Cold Brew Tonic!", "suggestedItem": {"name": "Cold Brew Citrus Tonic", "price": 220}, "text": "Add a Cold Brew Iced Tonic (+ ₹220) for a refreshing morning kick."}, display_order=2),
                ConceptMenuItem(concept_id="cafe", name="Truffle Brioche Scramble", price=420, desc="Organic pasture eggs, black truffle paste on brioche.", category="Brunch & Bakery", upsell={"message": "⭐ Complete with an artisanal espresso pairing.", "suggestedItem": {"name": "Double Espresso Macchiato", "price": 190}, "text": "Upgrade to a Double Espresso Macchiato (+ ₹190) for the ultimate pairing."}, display_order=3),
                ConceptMenuItem(concept_id="cafe", name="Cardamom Pistachio Babka", price=260, desc="Slow-proved twisted sourdough loaf with pistachio cream.", category="Brunch & Bakery", display_order=4),
            ])

            c2 = MenuConcept(
                id="steakhouse",
                name="Prime 88 Steakhouse",
                concept="Dry-Aged Cuts, Fine Wine & Truffles",
                accent_color="#ef4444",
                vibe="Fine Dining Luxury",
                title="Prime 88 Steakhouse",
                tagline="Table #04 • Luxury Dining",
                categories=["All", "Prime Cuts", "Starters & Sides", "Reserve Cellar"],
                display_order=2,
            )
            session.add(c2)
            await session.flush()

            session.add_all([
                ConceptMenuItem(concept_id="steakhouse", name="45-Day Dry-Aged Ribeye (14oz)", price=1850, desc="USDA Prime, bone marrow herb butter, smoked salt.", category="Prime Cuts", upsell={"message": "🍷 Master Sommelier: This cut pairs exceptionally with our Reserve Cabernet.", "suggestedItem": {"name": "Reserve Cabernet Sauvignon (Glass)", "price": 650}, "text": "Would you like to pair with a glass of Reserve Cabernet (+ ₹650)?"}, display_order=1),
                ConceptMenuItem(concept_id="steakhouse", name="Pan-Seared Chilean Sea Bass", price=1450, desc="Saffron beurre blanc, glazed baby fennel.", category="Prime Cuts", upsell={"message": "🍷 Pairing Recommendation: Chilled French Chablis balances the rich fish.", "suggestedItem": {"name": "French Chablis Premier Cru", "price": 550}, "text": "Best paired with a chilled glass of French Chablis (+ ₹550)."}, display_order=2),
                ConceptMenuItem(concept_id="steakhouse", name="Black Truffle Risotto", price=850, desc="Acquerello carnaroli, 24-month Parmigiano-Reggiano.", category="Starters & Sides", upsell={"message": "⭐ Chef Selection: Add Crispy Parmesan Truffle Fries for the table!", "suggestedItem": {"name": "Crispy Parmesan Truffle Fries", "price": 320}, "text": "Complete your table with Crispy Parmesan Truffle Fries (+ ₹320)."}, display_order=3),
                ConceptMenuItem(concept_id="steakhouse", name="Valrhona Chocolate Lava Cake", price=450, desc="Warm molten 70% dark chocolate, vanilla bean gelato.", category="Starters & Sides", display_order=4),
            ])

        await session.commit()
        logger.info("Marketing content verified and initialized in PostgreSQL.")
    except Exception as e:
        logger.warning(f"Content seeding notice: {e}")
        await session.rollback()
