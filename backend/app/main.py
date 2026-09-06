import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import create_tables
from backend.app.seed.run_seed import seed_database
from backend.app.controllers.peripheral_controller import router as peripheral_router
from backend.app.controllers.code_controller import router as code_router
from backend.app.controllers.health_controller import router as health_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("arduino_backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables are created and seed data is populated
    logger.info("Initializing database tables...")
    create_tables()
    logger.info("Checking / populating seed data...")
    try:
        seed_database()
    except Exception as e:
        logger.error(f"Seed initialization error: {e}")
    yield
    # Shutdown
    logger.info("FastAPI backend shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="RESTful Backend Controller for the ATmega2560 Arduino Learning Platform",
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers under /api/v1
app.include_router(peripheral_router, prefix=settings.API_V1_STR)
app.include_router(code_router, prefix=settings.API_V1_STR)
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(health_router)  # Also root /health


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Arduino Codes Made Easy API (ATmega2560)",
        "docs": "/docs",
        "api_v1": settings.API_V1_STR,
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)
