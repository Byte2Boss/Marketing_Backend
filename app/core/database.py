import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
from app.core.config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

# Determine active database engine
try:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
        pool_pre_ping=True,
    )
except Exception as e:
    logger.warning(f"Failed to initialize PostgreSQL async engine: {e}. Falling back to SQLite async engine.")
    engine = create_async_engine(
        settings.FALLBACK_SQLITE_URL,
        echo=settings.DEBUG,
        future=True,
    )

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for providing an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Create all database tables on startup and seed initial marketing content."""
    global engine, AsyncSessionLocal
    import app.models  # Ensure all SQLAlchemy models are registered on Base.metadata

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully in PostgreSQL.")
        
        # Seed content tables
        from app.services.content_seeder import seed_initial_content
        async with AsyncSessionLocal() as session:
            await seed_initial_content(session)
    except Exception as e:
        logger.warning(f"Could not initialize PostgreSQL tables: {e}. Attempting SQLite fallback...")
        engine = create_async_engine(
            settings.FALLBACK_SQLITE_URL,
            echo=settings.DEBUG,
            future=True,
        )
        AsyncSessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized with fallback SQLite engine.")
        
        from app.services.content_seeder import seed_initial_content
        async with AsyncSessionLocal() as session:
            await seed_initial_content(session)

