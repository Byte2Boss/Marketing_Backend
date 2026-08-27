import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.database import init_db
from app.api.deps import limiter
from app.api.v1.router import api_v1_router
from app.schemas.common import APIResponse, ErrorDetail

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("restromind_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown events."""
    logger.info("Initializing RestroMind AI Marketing API & Database...")
    await init_db()
    yield
    logger.info("Shutting down RestroMind AI Marketing API...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Asynchronous REST API powering the RestroMind AI Marketing Website.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Attach rate limiter state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if settings.CORS_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Format Pydantic validation errors into standard APIResponse envelope."""
    errors = []
    for error in exc.errors():
        field = " -> ".join([str(loc) for loc in error.get("loc", [])])
        errors.append({"field": field, "message": error.get("msg")})

    return JSONResponse(
        status_code=422,
        content=APIResponse(
            success=False,
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Invalid request payload. Please check submitted fields.",
                details=errors,
            ),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch-all unexpected error handler."""
    logger.error(f"Unhandled error on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            success=False,
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected server error occurred. Please try again later.",
            ),
        ).model_dump(),
    )


# Register API v1 routes
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Root"])
async def root():
    """Root welcome endpoint with API documentation links."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "active",
        "documentation": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health",
    }
