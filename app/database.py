"""
Database configuration and session management.
AWS-ready: Supports PostgreSQL (RDS) and SQLite for local development.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database URL - supports both PostgreSQL (AWS RDS) and SQLite (local)
# For AWS: DATABASE_URL=postgresql://user:pass@host:5432/dbname
# For local: DATABASE_URL=sqlite:///./veganai.db (or leave empty for default)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./veganai.db"  # Default to SQLite for local development
)

# Create engine
# For SQLite, we need check_same_thread=False for FastAPI
# For PostgreSQL, this is not needed
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False  # Set to True for SQL query debugging
    )
else:
    # PostgreSQL (AWS RDS)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using (important for RDS)
        echo=False
    )

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for FastAPI to get database session.
    Usage in endpoints:
        def my_endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - creates all tables.
    Call this once at startup or use Alembic migrations instead.
    """
    Base.metadata.create_all(bind=engine)

