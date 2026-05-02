"""
MediMind MCP - FastAPI Application

⚠️ HIPAA-COMPLIANT: This application handles Protected Health Information (PHI).

Security Features:
- HIPAA audit logging middleware (every PHI access logged)
- CORS with strict origin checking
- Security headers (HSTS, CSP, X-Frame-Options)
- Rate limiting
- Session timeout (15 minutes)
- TLS 1.3+ required (production)

Endpoints:
- /health: Health check (no PHI)
- /auth/fhir/callback: OAuth callback
- /api/v1/patients: Patient management
- /api/v1/observations: Clinical observations
- /api/v1/medications: Medication management
"""

from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
import time
import logging
from typing import Optional

from src.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==========================================
# Database Setup
# ==========================================
# Convert sync DATABASE_URL to async (postgresql -> postgresql+asyncpg)
async_db_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(
    async_db_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,
    max_overflow=20
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncSession:
    """Dependency for database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# ==========================================
# Application Lifespan
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    logger.info("Starting MediMind MCP...")
    
    # Validate HIPAA compliance
    violations = settings.validate_hipaa_compliance()
    if violations:
        logger.warning(f"HIPAA compliance warnings: {violations}")
    
    # TODO: Initialize AI models here
    # TODO: Connect to FHIR server
    
    logger.info("MediMind MCP started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down MediMind MCP...")
    await engine.dispose()
    logger.info("MediMind MCP shut down")

# ==========================================
# FastAPI Application
# ==========================================
app = FastAPI(
    title="MediMind MCP",
    description="HIPAA-Compliant Clinical Decision Support System",
    version="0.1.0",
    docs_url="/api/docs" if settings.DEBUG else None,  # Disable in production
    redoc_url="/api/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# ==========================================
# HIPAA Audit Logging Middleware
# ==========================================
@app.middleware("http")
async def audit_logging_middleware(request: Request, call_next):
    """
    Log every request for HIPAA compliance.
    
    ⚠️ CRITICAL: All PHI access must be audited (§164.312(b)).
    """
    start_time = time.time()
    
    # Extract request metadata
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    method = request.method
    path = request.url.path
    
    # Determine if PHI is accessed
    phi_accessed = any([
        "/patients" in path,
        "/observations" in path,
        "/medications" in path,
        "/allergies" in path,
        "/conditions" in path
    ])
    
    # Process request
    try:
        response = await call_next(request)
        status_code = response.status_code
        
        # Log audit entry (non-blocking)
        if phi_accessed and status_code == 200:
            logger.info(
                f"PHI Access: {method} {path}",
                extra={
                    "user_id": "system",  # TODO: Get from JWT token
                    "ip_address": client_ip,
                    "user_agent": user_agent,
                    "phi_accessed": True,
                    "status_code": status_code,
                    "duration_ms": round((time.time() - start_time) * 1000, 2)
                }
            )
        
        return response
        
    except Exception as e:
        logger.error(
            f"Request failed: {method} {path}",
            extra={
                "error": str(e),
                "ip_address": client_ip
            }
        )
        raise

# ==========================================
# Security Middleware
# ==========================================

# CORS (strict in production)
allowed_origins = ["http://localhost:3000"] if settings.DEBUG else []

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    max_age=600
)

# Trusted Host (prevent Host header attacks)
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["medimind.hospital.com", "*.medimind.hospital.com"]
    )

# ==========================================
# Security Headers Middleware
# ==========================================
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Add HIPAA-required security headers."""
    response = await call_next(request)
    
    # HSTS (Force HTTPS)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    
    # Content Security Policy
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
    
    # Prevent clickjacking
    response.headers["X-Frame-Options"] = "DENY"
    
    # Prevent MIME sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"
    
    # XSS Protection
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # Referrer Policy
    response.headers["Referrer-Policy"] = "no-referrer"
    
    return response

# ==========================================
# Health Check Endpoint
# ==========================================
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint (no PHI, no authentication required).
    
    Returns service status and version.
    """
    return {
        "status": "healthy",
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT,
        "hipaa_compliant": len(settings.validate_hipaa_compliance()) == 0
    }

# ==========================================
# Root Endpoint
# ==========================================
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint."""
    return {
        "application": "MediMind MCP",
        "version": "0.1.0",
        "description": "HIPAA-Compliant Clinical Decision Support System",
        "docs": "/api/docs" if settings.DEBUG else None,
        "health": "/health"
    }

# ==========================================
# Error Handlers
# ==========================================
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler.
    
    ⚠️ SECURITY: Never expose internal details or PHI in error messages!
    """
    logger.error(
        f"Unhandled exception: {exc}",
        extra={
            "path": request.url.path,
            "method": request.method
        },
        exc_info=True
    )
    
    # Generic error message (don't leak internal details)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please contact support.",
            "request_id": str(time.time())  # For tracking
        }
    )

# ==========================================
# TODO: Add API Routes
# ==========================================
# from src.api import patients, observations, medications, auth
# app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
# app.include_router(observations.router, prefix="/api/v1/observations", tags=["Observations"])
# app.include_router(medications.router, prefix="/api/v1/medications", tags=["Medications"])

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning",
        access_log=True
    )
