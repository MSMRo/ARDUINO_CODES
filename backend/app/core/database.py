import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from backend.app.core.config import settings

logger = logging.getLogger("arduino_backend")

db_url = settings.get_database_url()
is_sqlite = False

try:
    # Attempt to connect to PostgreSQL with a short connection timeout
    if "postgresql" in db_url:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 3}
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info(f"Successfully connected to PostgreSQL at {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
    else:
        engine = create_engine(db_url)
except Exception as e:
    logger.warning(
        f"Could not connect to PostgreSQL ({e}). Falling back to local SQLite database 'arduino_mega.db' for development/demo mode."
    )
    db_url = "sqlite:///./arduino_mega.db"
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    is_sqlite = True

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)
