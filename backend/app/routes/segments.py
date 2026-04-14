from fastapi import APIRouter, HTTPException
from app.services.segmentation_service import segmentation_service

router = APIRouter()

@router.get("")
async def get_segments():
    """Get customer segments"""
    try:
        segmentation = segmentation_service.get_segmentation()
        
        # Convert to list of dictionaries
        segments = [
            {
                "customer_id": str(row[0]),
                "segment": int(row[1])
            }
            for row in segmentation.values.tolist()
        ]
        
        return {
            "segments": segments,
            "total_customers": len(segments)
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))