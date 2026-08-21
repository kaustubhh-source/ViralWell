import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

def train_outbreak_model():
    # Resolve paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(script_dir, "..", "data", "raw", "mumbai_climate_health.csv"))
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Mock data not found at {data_path}. Please run generate_mock_data.py first.")
        
    print(f"Loading dataset from: {data_path}")
    df = pd.read_csv(data_path, parse_dates=["Date"], index_col="Date")
    
    # Feature engineering: shift Rainfall_mm by 21 days
    print("Feature engineering: creating 'Rainfall_Lag_21' column...")
    df["Rainfall_Lag_21"] = df["Rainfall_mm"].shift(21)
    
    # Drop rows with NaN values resulting from the lag shift
    df = df.dropna()
    print(f"Dataset shape after dropping NaN rows: {df.shape}")
    
    # Define features (X) and target (y)
    feature_cols = ["Temperature_C", "Humidity_Pct", "Rainfall_Lag_21"]
    target_col = "Viral_Cases"
    
    X = df[feature_cols]
    y = df[target_col]
    
    # Split the dataset: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Train the Random Forest Regressor model
    print("Training Random Forest Regressor model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("\n--- Model Evaluation ---")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"R-squared (R2) Score:     {r2:.4f}")
    print("------------------------\n")
    
    # Save the model
    model_path = os.path.join(script_dir, "outbreak_model.pkl")
    joblib.dump(model, model_path)
    print(f"Model successfully saved to: {model_path}")

if __name__ == "__main__":
    train_outbreak_model()
