from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.core.database import get_db, engine, is_sqlite
from backend.app.core.config import settings
from backend.app.models.peripheral import Peripheral, CodeExample

router = APIRouter(tags=["System Health"])


@router.get("/health", summary="System health and database status")
def health_check(db: Session = Depends(get_db)):
    """Check API server, database connectivity, and return content statistics."""
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"unreachable ({e})"

    peripherals_count = 0
    codes_count = 0
    try:
        peripherals_count = db.query(Peripheral).count()
        codes_count = db.query(CodeExample).count()
    except Exception:
        pass

    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "database": {
            "status": db_status,
            "engine_dialect": engine.dialect.name,
            "is_sqlite_fallback": is_sqlite,
            "url_host": settings.POSTGRES_HOST if not is_sqlite else "local sqlite",
        },
        "stats": {
            "total_peripherals": peripherals_count,
            "total_code_examples": codes_count
        }
    }
