from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_router

app = FastAPI(
    title="Business Decision Intelligence System API",
    description="API for business analytics and decision simulation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Business Decision Intelligence System API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}