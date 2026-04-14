from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.simulation_service import simulation_service

router = APIRouter()

class SimulationInput(BaseModel):
    price_change: float
    marketing_boost: float

@router.post("")
async def simulate_business_decision(input_data: SimulationInput):
    """Simulate impact of business decisions on revenue"""
    try:
        result = simulation_service.simulate(
            price_change=input_data.price_change,
            marketing_boost=input_data.marketing_boost
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))