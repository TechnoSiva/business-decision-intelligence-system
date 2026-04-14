from fastapi import APIRouter
from app.routes.summary import router as summary_router
from app.routes.forecast import router as forecast_router
from app.routes.segments import router as segments_router
from app.routes.simulation import router as simulation_router

api_router = APIRouter()

api_router.include_router(summary_router, prefix="/summary", tags=["summary"])
api_router.include_router(forecast_router, prefix="/forecast", tags=["forecast"])
api_router.include_router(segments_router, prefix="/segments", tags=["segments"])
api_router.include_router(simulation_router, prefix="/simulate", tags=["simulation"])