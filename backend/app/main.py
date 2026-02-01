"""
Main FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.core.config import settings
from app.core.database import engine, Base

# Import Routers
from app.modules.organization import debug_routes
from app.modules.organization import routes as organization_routes
from app.modules.files import routes as file_routes
from app.modules.calendar import router as calendar_router
from app.modules.test_management import routes as test_management_routes
from app.modules.projects import routes as projects_routes
from app.modules.inventory import routes as inventory_routes
from app.modules.quality_assurance import routes as quality_assurance_routes

# New Routers
from app.modules.rfqs.routes import router as rfq_router
from app.modules.estimations.routes import router as estimation_router
from app.modules.certification.routes import router as certifications_router
from app.modules.audits_section.routes import router as audit_router
from app.modules.ncrs.routes import router as ncr_router
from app.modules.samples.routes import router as samples_router
from app.modules.trf.routes import router as trfs_router
from app.modules.reports.routes import router as reports_router
from app.modules.document.routes import router as documents_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("[+] Starting up LMS Backend...")
    
    # Create upload directories if they don't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "logos"), exist_ok=True)
    os.makedirs(os.path.join(settings.UPLOAD_DIR, "documents"), exist_ok=True)
    
    # Create database tables (in production, use Alembic migrations)
    Base.metadata.create_all(bind=engine)
    
    print("[+] Startup complete!")
    
    yield
    
    # Shutdown
    print("[-] Shutting down LMS Backend...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for Laboratory Management System",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS Middleware - Allow all localhost ports for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(
    debug_routes.router,
    prefix="/api/v1/organizations",
    tags=["Debug"]
)

app.include_router(
    organization_routes.router,
    prefix="/api/v1/organizations",
    tags=["Organizations"]
)

app.include_router(
    file_routes.router,
    prefix="/api/v1/files",
    tags=["Files"]
)

app.include_router(
    calendar_router,
    prefix="/api/v1",
    tags=["Calendar"]
)

app.include_router(
    test_management_routes.router,
    prefix="/api/v1",
    tags=["Test Management"]
)

app.include_router(
    projects_routes.router,
    prefix="/api/v1",
    tags=["Projects & Customers"]
)

app.include_router(
    inventory_routes.router,
    prefix="/api/v1",
    tags=["Inventory Management"]
)

app.include_router(
    quality_assurance_routes.router,
    prefix="/api/v1",
    tags=["Quality Assurance"]
)

# New Modules
app.include_router(rfq_router, prefix="/api/v1", tags=["RFQs"])
app.include_router(estimation_router, prefix="/api/v1", tags=["Estimations"])
app.include_router(certifications_router, prefix="/api/v1", tags=["Certifications"])
app.include_router(audit_router, prefix="/api/v1", tags=["Audits Section"])
app.include_router(ncr_router, prefix="/api/v1", tags=["NCRS"])
app.include_router(samples_router, prefix="/api/v1", tags=["Samples"])
app.include_router(trfs_router, prefix="/api/v1", tags=["TRFs"])
app.include_router(reports_router, prefix="/api/v1", tags=["Reports"])
app.include_router(documents_router, prefix="/api/v1", tags=["Documents (Extended)"])

from app.modules.scope_management.routes import router as scope_management_router
app.include_router(scope_management_router, prefix="/api/v1/scope-management", tags=["Scope Management"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to LMS Backend API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
