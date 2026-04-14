from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pandas as pd
from app.services.data_loader import data_loader

class ModelService:
    _instance = None
    _model = None
    _feature_columns = None
    _target_column = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelService, cls).__new__(cls)
        return cls._instance
    
    def train_model(self):
        """Train a regression model for revenue forecasting"""
        if self._model is not None:
            return self._model
        
        # Get the cleaned data
        df = data_loader.get_data()
        
        # Identify target column (revenue or equivalent)
        target_column = None
        for col in ['revenue', 'sales', 'income']:
            if col in df.columns:
                target_column = col
                break
        
        if not target_column:
            raise ValueError("No revenue column found in the dataset")
        
        # Identify feature columns
        feature_columns = ['Month', 'Year']
        
        # Add quantity-related columns if they exist
        for col in ['units_sold', 'quantity', 'units']:
            if col in df.columns:
                # Ensure it's numeric
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    feature_columns.append(col)
                except:
                    pass
        
        # Check if all feature columns exist
        missing_features = [col for col in feature_columns if col not in df.columns]
        if missing_features:
            raise ValueError(f"Missing feature columns: {missing_features}")
        
        # Prepare data
        X = df[feature_columns]
        y = df[target_column]
        
        # Ensure target is numeric
        try:
            y = pd.to_numeric(y, errors='coerce')
        except:
            raise ValueError(f"Target column {target_column} cannot be converted to numeric")
        
        # Remove rows with NaN values
        X = X.dropna()
        y = y[X.index]
        
        if len(X) < 10:
            raise ValueError("Not enough data to train the model")
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f"Model trained successfully. MSE: {mse:.2f}")
        print(f"Feature columns: {feature_columns}")
        print(f"Target column: {target_column}")
        
        # Store the model and columns
        self._model = model
        self._feature_columns = feature_columns
        self._target_column = target_column
        
        return model
    
    def predict(self, input_data):
        """Make predictions using the trained model"""
        if self._model is None:
            self.train_model()
        
        # Validate input data
        for col in self._feature_columns:
            if col not in input_data:
                raise ValueError(f"Missing required feature: {col}")
        
        # Create a DataFrame for prediction
        input_df = pd.DataFrame([input_data])
        
        # Ensure numeric types
        for col in self._feature_columns:
            try:
                input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            except:
                raise ValueError(f"Feature {col} must be numeric")
        
        # Check for NaN values
        if input_df.isnull().any().any():
            raise ValueError("Input data contains non-numeric values")
        
        # Make prediction
        prediction = self._model.predict(input_df)
        
        return {
            "prediction": float(prediction[0]),
            "feature_columns": self._feature_columns,
            "target_column": self._target_column
        }

# Create a global instance
model_service = ModelService()