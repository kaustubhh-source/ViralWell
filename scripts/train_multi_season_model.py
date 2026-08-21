import os
import sys
import subprocess
import json
import numpy as np
import pandas as pd
import joblib

# 1. Environment Setup - Ensure xgboost is installed dynamically if missing
try:
    import xgboost as xgb
except ImportError:
    print("XGBoost is missing. Installing dynamically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "xgboost"])
    import xgboost as xgb

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

def train_advanced_pipeline():
    np.random.seed(42)
    
    # Resolve paths relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))
    models_dir = os.path.abspath(os.path.join(script_dir, "..", "models"))
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    
    historical_path = os.path.join(data_dir, "historical_mumbai_weather.csv")
    if not os.path.exists(historical_path):
        raise FileNotFoundError(f"Historical weather dataset not found at {historical_path}. Please run fetch_historical_weather.py first.")
        
    print(f"Loading weather dataset: {historical_path}")
    base_df = pd.read_csv(historical_path)
    
    # 2. Unsupervised Clustering Engine & Microclimate Simulation
    print("Simulating microclimate variations across 5 key Mumbai regions...")
    regions = [
        {"name": "Chembur", "lat": 19.0622, "lon": 72.8984, "temp_offset": 0.5, "humidity_offset": -2.0, "rain_offset": 0.0},
        {"name": "Dadar", "lat": 19.0178, "lon": 72.8478, "temp_offset": 0.0, "humidity_offset": 0.0, "rain_offset": 0.0},
        {"name": "Andheri", "lat": 19.1136, "lon": 72.8697, "temp_offset": -0.2, "humidity_offset": 3.0, "rain_offset": 2.0},
        {"name": "Colaba", "lat": 18.9067, "lon": 72.8147, "temp_offset": -0.8, "humidity_offset": 5.0, "rain_offset": 0.0},
        {"name": "Borivali", "lat": 19.2307, "lon": 72.8567, "temp_offset": -0.5, "humidity_offset": -1.0, "rain_offset": 0.0}
    ]
    
    dfs = []
    for r in regions:
        df_r = base_df.copy()
        df_r["Region"] = r["name"]
        df_r["Latitude"] = r["lat"]
        df_r["Longitude"] = r["lon"]
        df_r["Max_Temperature_C"] = df_r["Max_Temperature_C"] + r["temp_offset"]
        df_r["Mean_Humidity_Pct"] = (df_r["Mean_Humidity_Pct"] + r["humidity_offset"]).clip(30, 100)
        df_r["Daily_Rain_mm"] = (df_r["Daily_Rain_mm"] + r["rain_offset"]).clip(lower=0)
        dfs.append(df_r)
        
    df_clustered = pd.concat(dfs, ignore_index=True)
    df_clustered["Date"] = pd.to_datetime(df_clustered["Date"])
    
    print("Grouping by region stats and fitting KMeans model...")
    # Group by region to run unsupervised clustering on geographical climate signals
    region_stats = df_clustered.groupby("Region").agg({
        "Latitude": "first",
        "Longitude": "first",
        "Max_Temperature_C": "mean",
        "Mean_Humidity_Pct": "mean",
        "Daily_Rain_mm": "mean"
    }).reset_index()
    
    scaler = StandardScaler()
    cluster_features = region_stats[["Latitude", "Longitude", "Max_Temperature_C", "Mean_Humidity_Pct", "Daily_Rain_mm"]]
    scaled_features = scaler.fit_transform(cluster_features)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    region_stats["Cluster_ID"] = kmeans.fit_predict(scaled_features)
    
    # Programmatic cluster labeling based on feature values
    uhi_cluster = region_stats.loc[region_stats["Max_Temperature_C"].idxmax()]["Cluster_ID"]
    waterlogging_cluster = region_stats.loc[region_stats["Daily_Rain_mm"].idxmax()]["Cluster_ID"]
    all_clusters = {0, 1, 2}
    stable_cluster = list(all_clusters - {uhi_cluster, waterlogging_cluster})[0]
    
    cluster_mapping = {
        uhi_cluster: "Urban Heat Island Risk",
        waterlogging_cluster: "Waterlogging Vectors Risk",
        stable_cluster: "Stable Microclimate Risk"
    }
    region_stats["Cluster_Zone"] = region_stats["Cluster_ID"].map(cluster_mapping)
    
    # Save the trained KMeans model and label mappings
    kmeans_path = os.path.join(models_dir, "vulnerability_clusters.pkl")
    joblib.dump({"model": kmeans, "scaler": scaler, "mapping": cluster_mapping}, kmeans_path)
    print(f"KMeans model successfully saved to: {kmeans_path}")
    
    # Map Cluster labels back to the full dataset
    df_clustered = df_clustered.merge(region_stats[["Region", "Cluster_ID", "Cluster_Zone"]], on="Region", how="left")
    
    # Compute region-specific 21-day rolling rainfall sum to avoid cross-region leakage
    print("Calculating rolling 21-day lag rainfall parameters...")
    df_clustered = df_clustered.sort_values(by=["Region", "Date"])
    df_clustered["Rainfall_Lag_21"] = df_clustered.groupby("Region")["Daily_Rain_mm"].transform(
        lambda x: x.rolling(window=21).sum()
    )
    df_clustered = df_clustered.dropna()
    df_clustered["Month"] = df_clustered["Date"].dt.month
    
    # Simulate PM2.5 AQI parameter based on winter season and temperature
    is_winter_sim = np.isin(df_clustered["Month"].values, [10, 11, 12, 1, 2]).astype(float)
    df_clustered["PM25_Index"] = 15.0 + 85.0 * is_winter_sim * (35.0 - df_clustered["Max_Temperature_C"]) / 15.0 + np.random.normal(0, 5, len(df_clustered))
    df_clustered["PM25_Index"] = df_clustered["PM25_Index"].clip(5.0, 150.0)
    
    # Output clustered dataset
    clustered_csv_path = os.path.join(data_dir, "mumbai_clustered_health_data.csv")
    df_clustered.to_csv(clustered_csv_path, index=False)
    print(f"Clustered dataset exported successfully to: {clustered_csv_path}")
    
    # 3. Target Simulation based on Weather & Seasons
    print("Simulating target cases for diseases...")
    # ponytail: synthetic target counts generated via Poisson rules; upgrade to factual health register data for clinical use.
    months = df_clustered["Month"].values
    temp = df_clustered["Max_Temperature_C"].values
    humidity = df_clustered["Mean_Humidity_Pct"].values
    rain_lag = df_clustered["Rainfall_Lag_21"].values
    rain_daily = df_clustered["Daily_Rain_mm"].values
    pm25 = df_clustered["PM25_Index"].values
    
    is_summer = np.isin(months, [3, 4, 5]).astype(float)
    is_monsoon = np.isin(months, [6, 7, 8, 9]).astype(float)
    is_winter = np.isin(months, [10, 11, 12, 1, 2]).astype(float)
    
    # Gastroenteritis Cases
    gastro_exp = 3.0 + is_summer * 12.0 * np.clip(temp - 32.0, 0, None) + is_monsoon * 5.0 * (rain_daily > 10.0).astype(float)
    df_clustered["Gastroenteritis_Cases"] = np.random.poisson(gastro_exp)
    
    # Heatstroke Cases
    heatstroke_exp = 0.2 + is_summer * 15.0 * np.clip(temp - 34.0, 0, None)
    df_clustered["Heatstroke_Cases"] = np.random.poisson(heatstroke_exp)
    
    # Dengue Cases
    dengue_exp = 0.5 + is_monsoon * 0.25 * rain_lag * (humidity > 80.0).astype(float)
    df_clustered["Dengue_Cases"] = np.random.poisson(dengue_exp)
    
    # Malaria Cases
    malaria_exp = 0.3 + is_monsoon * 0.18 * rain_lag * (humidity > 80.0).astype(float)
    df_clustered["Malaria_Cases"] = np.random.poisson(malaria_exp)
    
    # Influenza Cases tuned by PM25_Index
    influenza_exp = 2.0 + is_winter * (0.8 * np.clip(33.0 - temp, 0, None) * np.clip(80.0 - humidity, 0, None) / 5.0) + (pm25 / 30.0)
    df_clustered["Influenza_Cases"] = np.random.poisson(influenza_exp)
    
    # Bronchitis Cases tuned heavily by PM25_Index
    bronchitis_exp = 1.5 + is_winter * (0.6 * np.clip(33.0 - temp, 0, None) * np.clip(80.0 - humidity, 0, None) / 5.0) + 2.5 * (pm25 / 25.0)
    df_clustered["Bronchitis_Respiratory_Cases"] = np.random.poisson(bronchitis_exp)
    
    # Define Inputs and Outputs (6 features including PM25_Index)
    feature_cols = ["Max_Temperature_C", "Mean_Humidity_Pct", "Daily_Rain_mm", "Rainfall_Lag_21", "Month", "PM25_Index"]
    target_cols = [
        "Gastroenteritis_Cases", "Heatstroke_Cases", "Dengue_Cases",
        "Malaria_Cases", "Influenza_Cases", "Bronchitis_Respiratory_Cases"
    ]
    
    X = df_clustered[feature_cols]
    y = df_clustered[target_cols]
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Automated Hyperparameter Tuning
    print("Running GridSearchCV for RandomForest hyperparameter tuning...")
    param_grid = {
        'estimator__n_estimators': [50, 100],
        'estimator__max_depth': [None, 10],
        'estimator__min_samples_split': [2, 5]
    }
    base_rf = RandomForestRegressor(random_state=42, n_jobs=-1)
    multi_rf = MultiOutputRegressor(base_rf)
    grid_search = GridSearchCV(multi_rf, param_grid, cv=3, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    best_rf = grid_search.best_estimator_
    print(f"Optimal RF Parameters discovered: {grid_search.best_params_}")
    
    # 5. Multi-Model Benchmarking
    print("Running multi-model benchmark evaluation suite...")
    models = {
        "Linear Regression (Baseline)": MultiOutputRegressor(LinearRegression()),
        "Optimized Random Forest": best_rf,
        "Multi-Output XGBoost": MultiOutputRegressor(xgb.XGBRegressor(n_estimators=100, random_state=42, n_jobs=-1))
    }
    
    benchmark_metrics = {}
    best_model_name = None
    best_r2 = -float("inf")
    
    for name, model in models.items():
        print(f"  Fitting {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = root_mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        benchmark_metrics[name] = {
            "MAE": float(mae),
            "RMSE": float(rmse),
            "R2": float(r2)
        }
        print(f"  --> Metrics: MAE={mae:.4f}, RMSE={rmse:.4f}, R²={r2:.4f}")
        
        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            
    print(f"\nBest Performing Architecture: {best_model_name} (R² = {best_r2:.4f})")
    
    # 6. Artifact Export
    best_model_path = os.path.join(models_dir, "viralwell_multi_season_model.pkl")
    joblib.dump(models[best_model_name], best_model_path)
    print(f"Best model exported to binary: {best_model_path}")
    
    benchmark_json_path = os.path.join(models_dir, "benchmark_metrics.json")
    with open(benchmark_json_path, "w") as f:
        json.dump(benchmark_metrics, f, indent=4)
    print(f"Competitive benchmark JSON metadata saved to: {benchmark_json_path}")

if __name__ == "__main__":
    train_advanced_pipeline()
