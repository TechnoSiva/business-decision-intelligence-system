import pandas as pd
from app.services.data_loader import data_loader

class SimulationService:
    _instance = None
    _base_revenue = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimulationService, cls).__new__(cls)
        return cls._instance
    
    def get_base_revenue(self):
        """Calculate base revenue from the dataset"""
        if self._base_revenue is not None:
            return self._base_revenue
        
        # Get the cleaned data
        df = data_loader.get_data()
        
        # Find revenue column
        revenue_column = None
        for col in ['revenue', 'sales', 'income']:
            if col in df.columns:
                revenue_column = col
                break
        
        if not revenue_column:
            raise ValueError("No revenue column found in the dataset")
        
        # Calculate average revenue
        base_revenue = df[revenue_column].mean()
        print(f"Base revenue calculated: ${base_revenue:.2f}")
        
        self._base_revenue = base_revenue
        return base_revenue
    
    def simulate(self, price_change, marketing_boost):
        """Simulate impact of business decisions on revenue"""
        # Validate inputs
        if not isinstance(price_change, (int, float)):
            raise ValueError("price_change must be a number")
        
        if not isinstance(marketing_boost, (int, float)):
            raise ValueError("marketing_boost must be a number")
        
        # Get base revenue
        base_revenue = self.get_base_revenue()
        
        # Apply simulation formula
        # Logic: Demand decreases with price increase, increases with marketing
        predicted_revenue = base_revenue * (1 - price_change * 0.5 + marketing_boost * 0.3)
        
        # Calculate impact
        revenue_change = predicted_revenue - base_revenue
        percent_change = (revenue_change / base_revenue) * 100
        
        return {
            "base_revenue": base_revenue,
            "price_change": price_change,
            "marketing_boost": marketing_boost,
            "predicted_revenue": predicted_revenue,
            "revenue_change": revenue_change,
            "percent_change": percent_change,
            "formula": "predicted_revenue = base_revenue * (1 - price_change*0.5 + marketing_boost*0.3)"
        }

# Create a global instance
simulation_service = SimulationService()