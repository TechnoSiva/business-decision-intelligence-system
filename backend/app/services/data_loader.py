import pandas as pd
import os
from datetime import datetime

class DataLoader:
    _instance = None
    _data = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
        return cls._instance
    
    def load_data(self):
        """Load and clean the sales data from CSV"""
        if self._data is not None:
            return self._data
        
        # Get the data file path
        data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        data_file = os.path.join(data_dir, 'sales_data.csv')
        
        # Load the CSV file
        try:
            df = pd.read_csv(data_file)
            print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns")
            print(f"Column names: {list(df.columns)}")
            
            # Inspect columns for date parsing
            date_columns = []
            for col in df.columns:
                # Try to parse as date
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_columns.append(col)
                    print(f"Parsed '{col}' as date column")
                except:
                    pass
            
            # Remove nulls
            null_count = df.isnull().sum().sum()
            if null_count > 0:
                df = df.dropna()
                print(f"Removed {null_count} null values")
            
            # Remove duplicates
            duplicate_count = len(df) - len(df.drop_duplicates())
            if duplicate_count > 0:
                df = df.drop_duplicates()
                print(f"Removed {duplicate_count} duplicate rows")
            
            # Add Month and Year columns if date columns exist
            if date_columns:
                # Use the first date column found
                date_col = date_columns[0]
                df['Month'] = df[date_col].dt.month
                df['Year'] = df[date_col].dt.year
                print(f"Added Month and Year columns from {date_col}")
            
            print(f"Final dataset: {len(df)} rows")
            self._data = df
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def get_data(self):
        """Get the cleaned data"""
        if self._data is None:
            return self.load_data()
        return self._data

# Create a global instance
data_loader = DataLoader()