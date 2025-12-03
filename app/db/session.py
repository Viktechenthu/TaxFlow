# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# What is this?
# ─────────────
# This file sets up the connection to your PostgreSQL database

# Create database engine
# ──────────────────────
# The engine is like a "connection pool" to your database
engine = create_engine(
    settings.DATABASE_URL,
    # echo=True will print all SQL commands (useful for learning!)
    echo=True,
    # Connection pool settings
    pool_pre_ping=True,  # Test connections before using them
    pool_size=5,          # Keep 5 connections ready
    max_overflow=10       # Allow up to 10 extra connections if needed
)

# Create SessionLocal class
# ─────────────────────────
# A Session is like a "workspace" where you interact with the database
# Each request will create its own session
SessionLocal = sessionmaker(
    autocommit=False,  # Don't auto-save changes
    autoflush=False,   # Don't auto-send changes to DB
    bind=engine        # Connect to our engine
)

# Create Base class
# ─────────────────
# All your database models will inherit from this
Base = declarative_base()

# Dependency function for FastAPI
# ────────────────────────────────
def get_db():
    """
    Create a new database session for each request
    Automatically closes the session when done
    
    Usage in FastAPI:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    """
    db = SessionLocal()
    try:
        yield db  # Give the session to the request
    finally:
        db.close()  # Always close when done

# Helper function to get a session (for scripts)
def get_db_session():
    """
    Get a database session for use in scripts/workers
    Remember to close it when done!
    
    Usage:
        db = get_db_session()
        try:
            users = db.query(User).all()
        finally:
            db.close()
    """
    return SessionLocal()