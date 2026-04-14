from sklearn.cluster import KMeans
import pandas as pd
from app.services.data_loader import data_loader

class SegmentationService:
    _instance = None
    _segmentation_result = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SegmentationService, cls).__new__(cls)
        return cls._instance
    
    def segment_customers(self, n_clusters=3):
        """Segment customers using KMeans clustering"""
        if self._segmentation_result is not None:
            return self._segmentation_result
        
        # Get the cleaned data
        df = data_loader.get_data()
        
        # Check for Customer_ID column
        customer_id_column = None
        for col in ['Customer_ID', 'customer_id', 'customerId', 'CustomerId']:
            if col in df.columns:
                customer_id_column = col
                break
        
        if not customer_id_column:
            raise ValueError("No Customer_ID column found in the dataset")
        
        # Check for revenue and quantity columns
        revenue_column = None
        for col in ['revenue', 'sales', 'income']:
            if col in df.columns:
                revenue_column = col
                break
        
        quantity_column = None
        for col in ['units_sold', 'quantity', 'units']:
            if col in df.columns:
                quantity_column = col
                break
        
        if not revenue_column:
            raise ValueError("No revenue column found in the dataset")
        
        if not quantity_column:
            raise ValueError("No quantity column found in the dataset")
        
        # Aggregate by customer
        customer_agg = df.groupby(customer_id_column).agg({
            revenue_column: 'sum',
            quantity_column: 'sum'
        }).reset_index()
        
        # Prepare features for clustering
        features = customer_agg[[revenue_column, quantity_column]]
        
        # Handle any NaN values
        features = features.dropna()
        customer_agg = customer_agg.loc[features.index]
        
        if len(features) < n_clusters:
            raise ValueError(f"Not enough customers to create {n_clusters} segments")
        
        # Apply KMeans clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        customer_agg['segment'] = kmeans.fit_predict(features)
        
        print(f"Customer segmentation completed with {n_clusters} clusters")
        print(f"Total customers segmented: {len(customer_agg)}")
        
        # Store the result
        self._segmentation_result = customer_agg[[customer_id_column, 'segment']]
        
        return self._segmentation_result
    
    def get_segmentation(self):
        """Get the segmentation result"""
        if self._segmentation_result is None:
            return self.segment_customers()
        return self._segmentation_result

# Create a global instance
segmentation_service = SegmentationService()