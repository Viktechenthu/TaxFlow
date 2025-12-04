"""
TaxFlow AI - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import users
from app.core.config import settings

# Create FastAPI app
app = FastAPI(
    title="TaxFlow AI API",
    description="AI-powered tax receipt management system",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS middleware (allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

# Health check endpoint
@app.get("/health")
def health_check():
    """Check if API is running"""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "0.1.0"
    }

# Root endpoint
@app.get("/")
def root():
    """API root"""
    return {
        "message": "Welcome to TaxFlow AI API",
        "docs": "/docs",
        "health": "/health"
    }
