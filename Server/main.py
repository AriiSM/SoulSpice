from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.routes import router as api_router
from app.api import auth_routes

from app.core.config import settings

from app.core.database import Base, engine
from app.models import user, message

Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")
app.include_router(auth_routes.router, prefix="/api")

# Root endpoint for health check
@app.get("/")
async def root():
    return {
        "message": f"{settings.PROJECT_NAME} API is running",
        "status": "online",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    
# python main.py