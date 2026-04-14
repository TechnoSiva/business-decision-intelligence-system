from fastapi import APIRouter, HTTPException
from app.services.model_service import model_service

router = APIRouter()

@router.get("")
async def get_forecast():
    """Get predicted revenue for sample input"""
    try:
        # Sample input for forecast
        sample_input = {
            "Month": 6,
            "Year": 2023,
            "units_sold": 100
        }
        
        prediction = model_service.predict(sample_input)
        
        return {
            "sample_input": sample_input,
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))