
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.db.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not app.state.testing:
        create_tables()
    yield


def create_app(testing: bool = False) -> FastAPI:
    application = FastAPI(
        title="ReturnGuard API",
        description="Backend API for e-commerce returns and refunds",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.state.testing = testing
    application.include_router(api_router, prefix="/api/v1")

    @application.get("/health", tags=["Health"])
    def health_check():
        return {
            "status": "healthy",
            "application": "ReturnGuard",
        }
    return application


app = create_app()
