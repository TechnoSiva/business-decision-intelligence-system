from fastapi import APIRouter, HTTPException
from app.services.data_loader import data_loader

router = APIRouter()

@router.get("")
async def get_summary():
    """Get business summary including total revenue, top products, and region stats"""
    try:
        df = data_loader.get_data()
        
        # Calculate total revenue
        revenue_column = None
        for col in ['revenue', 'sales', 'income']:
            if col in df.columns:
                revenue_column = col
                break
        
        if not revenue_column:
            raise HTTPException(status_code=404, detail="No revenue column found in dataset")
        
        total_revenue = df[revenue_column].sum()
        
        # Get top products by revenue
        top_products = []
        if 'product_category' in df.columns:
            product_revenue = df.groupby('product_category')[revenue_column].sum().sort_values(ascending=False)
            top_products = [
                {"product": product, "revenue": float(revenue)}
                for product, revenue in product_revenue.head(5).items()
            ]
        
        # Get region stats
        region_stats = []
        if 'region' in df.columns:
            region_data = df.groupby('region').agg({
                revenue_column: 'sum',
                'units_sold': 'sum' if 'units_sold' in df.columns else 'count'
            }).reset_index()
            region_stats = [
                {
                    "region": row['region'],
                    "revenue": float(row[revenue_column]),
                    "units": float(row['units_sold'] if 'units_sold' in df.columns else row['units_sold'])
                }
                for _, row in region_data.iterrows()
            ]
        
        return {
            "total_revenue": float(total_revenue),
            "top_products": top_products,
            "region_stats": region_stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))