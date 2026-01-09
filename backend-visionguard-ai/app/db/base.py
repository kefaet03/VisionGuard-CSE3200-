"""
Database Configuration and Setup
PostgreSQL + SQLAlchemy setup for VisionGuard AI
"""

import os

# Load environment variables from .env when running scripts that import this module
# (e.g. one-off init commands). main.py also loads .env, so this is a safe fallback.
try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

# Database URL from environment variable or default.
# NOTE: Do not hardcode real credentials in source control.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/visionguard_db",
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    echo=False,  # Set to True for SQL query logging during development
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()


def get_db() -> Generator:
    """
    Dependency function to get database session
    Yields a database session and ensures it's closed after use

    Usage in FastAPI:
        @app.get("/endpoint")
        def endpoint(db: Session = Depends(get_db)):
            # Use db here
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables
    This should be called on application startup
    """
    # Import all models so they are registered on Base.metadata
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
