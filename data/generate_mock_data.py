import os
import numpy as np
import pandas as pd

def generate_mumbai_dataset(start_date="2021-01-01", end_date="2026-12-31"):
    """
    Generates a realistic daily climate and health dataset for Mumbai from 2021 to 2026.
    
    Mumbai Climate Seasons:
    - Winter (Dec-Feb): Cool and dry
    - Summer (Mar-May): Hot and humid
    - Monsoon (Jun-Sep): Heavy rainfall, very high humidity
    - Post-Monsoon (Oct-Nov): Warm and humid transition
    
    Health Indicators:
    - Mosquito_Density_Index (0-100): Depends on temperature suitability, humidity, and 14-day rainfall accumulation.
    - Viral_Cases: Represents seasonal outbreaks of Dengue/Malaria (vector-borne, lagging mosquito density) 
      and Flu (respiratory, peaking in monsoon and winter).
    """
    print(f"Generating mock data from {start_date} to {end_date}...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate date range
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    n_days = len(dates)
    
    df = pd.DataFrame(index=dates)
    df.index.name = "Date"
    
    # Define monthly norms for temperature (°C) and humidity (%)
    # Mumbai has a double peak in temperature: pre-monsoon (May) and post-monsoon (October)
    temp_norms = {
        1: 24.0, 2: 25.5, 3: 28.0, 4: 30.0, 5: 31.5, 6: 29.0,
        7: 27.2, 8: 27.0, 9: 27.5, 10: 29.0, 11: 28.0, 12: 25.5
    }
    
    humidity_norms = {
        1: 58, 2: 58, 3: 62, 4: 68, 5: 72, 6: 83,
        7: 88, 8: 88, 9: 85, 10: 75, 11: 67, 12: 60
    }
    
    # Rainfall probabilities and Gamma distribution parameters (shape, scale) per month
    # Mumbai receives massive rainfall during monsoons (June-September)
    rainfall_norms = {
        # Month: (prob_of_rain, shape, scale)
        1: (0.01, 0.5, 5.0),
        2: (0.01, 0.5, 5.0),
        3: (0.01, 0.5, 5.0),
        4: (0.02, 0.5, 8.0),
        5: (0.08, 0.8, 12.0),
        6: (0.68, 1.6, 22.0),  # Monsoon starts
        7: (0.88, 2.2, 28.0),  # Heavy monsoon peak
        8: (0.84, 2.0, 24.0),  # Heavy monsoon peak
        9: (0.64, 1.6, 20.0),  # Monsoon winds down
        10: (0.18, 1.0, 12.0), # Post-monsoon showers
        11: (0.04, 0.8, 8.0),
        12: (0.01, 0.5, 5.0)
    }
    
    # Map months to daily base norms
    months = df.index.month
    df["Month"] = months
    
    # Smooth baseline to avoid sudden step-changes at month boundaries
    df["Temp_Base"] = df["Month"].map(temp_norms)
    df["Temp_Base_Smooth"] = df["Temp_Base"].rolling(window=45, min_periods=1, center=True).mean()
    
    df["Humidity_Base"] = df["Month"].map(humidity_norms)
    df["Humidity_Base_Smooth"] = df["Humidity_Base"].rolling(window=45, min_periods=1, center=True).mean()
    
    # Add weather fluctuations
    # Daily temperature fluctuations
    df["Temperature_C"] = df["Temp_Base_Smooth"] + np.random.normal(0, 1.2, size=n_days)
    df["Temperature_C"] = df["Temperature_C"].round(1)
    
    # Daily humidity fluctuations
    df["Humidity_Pct"] = df["Humidity_Base_Smooth"] + np.random.normal(0, 3.5, size=n_days)
    df["Humidity_Pct"] = df["Humidity_Pct"].clip(30.0, 100.0).round(1)
    
    # Daily rainfall simulation
    rainfall = np.zeros(n_days)
    for idx, dt in enumerate(dates):
        month = dt.month
        prob, shape, scale = rainfall_norms[month]
        if np.random.rand() < prob:
            # Generate rain using Gamma distribution to get realistic positive skew (few very heavy rain days)
            rainfall[idx] = np.random.gamma(shape, scale)
            
    df["Rainfall_mm"] = np.round(rainfall, 1)
    
    # 2. Mosquito Density Index (0 - 100)
    # Depends on 14-day accumulated rainfall, temperature suitability, and humidity suitability.
    df["Acc_Rain_14d"] = df["Rainfall_mm"].rolling(window=14, min_periods=1).sum()
    
    # Temperature suitability: optimal breeding around 28°C
    temp_suitability = np.exp(-((df["Temperature_C"] - 28.0) / 4.5) ** 2)
    
    # Humidity suitability: higher humidity is better, sigmoidal relationship
    humidity_suitability = 1.0 / (1.0 + np.exp(-0.15 * (df["Humidity_Pct"] - 65.0)))
    
    # Rainfall suitability: stagnant water pools build up, but saturate above 100mm
    rain_suitability = df["Acc_Rain_14d"] / (df["Acc_Rain_14d"] + 60.0)
    
    # Combine suitability factors to get mosquito index baseline
    mosquito_base = 5.0 + 85.0 * temp_suitability * humidity_suitability * rain_suitability
    # Add daily variance
    df["Mosquito_Density_Index"] = mosquito_base + np.random.normal(0, 4.0, size=n_days)
    df["Mosquito_Density_Index"] = df["Mosquito_Density_Index"].clip(0.0, 100.0).round(1)
    
    # 3. Viral Cases (seasonal outbreaks of Dengue, Malaria, and Flu)
    # Vector-borne cases (Dengue/Malaria) peak ~2-3 weeks after mosquito surges
    # We use a 21-day lagged mosquito index
    df["Mosquito_Lagged"] = df["Mosquito_Density_Index"].shift(21).bfill().fillna(5.0)
    dengue_malaria_expected = 1.4 * df["Mosquito_Lagged"]
    
    # Flu cases: high humidity + rainy days create flu spikes, with a smaller dry winter peak
    flu_expected = 4.0
    # Monsoon flu component (June - Sept)
    is_monsoon = df["Month"].isin([6, 7, 8, 9]).astype(float)
    is_winter = df["Month"].isin([12, 1, 2]).astype(float)
    
    # Rainfall increases flu transmission (indoor crowding)
    rain_flu_modifier = (df["Rainfall_mm"] > 0).astype(float) * 12.0 * (df["Humidity_Pct"] / 100.0)
    flu_expected += is_monsoon * (8.0 + rain_flu_modifier)
    # Winter dry cold flu component
    flu_expected += is_winter * (10.0 * (30.0 - df["Temperature_C"]).clip(lower=0.0) / 10.0)
    
    # Total expected daily cases
    df["Expected_Cases"] = dengue_malaria_expected + flu_expected
    
    # Generate actual daily cases using Poisson distribution for realistic discrete counts
    df["Viral_Cases"] = np.random.poisson(df["Expected_Cases"])
    
    # Clean up intermediate columns before saving
    final_cols = ["Temperature_C", "Humidity_Pct", "Rainfall_mm", "Mosquito_Density_Index", "Viral_Cases"]
    final_df = df[final_cols]
    
    # Output file path
    # We should dynamically resolve data/raw relative to workspace root or file location
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "raw")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "mumbai_climate_health.csv")
    
    final_df.to_csv(output_path)
    print(f"Dataset successfully created and saved to: {output_path}")
    print(f"Total rows generated: {len(final_df)}")
    print(f"Date range: {final_df.index.min().strftime('%Y-%m-%d')} to {final_df.index.max().strftime('%Y-%m-%d')}")
    print("\nSample Data:")
    print(final_df.head())
    print("\nSummary Statistics:")
    print(final_df.describe())

if __name__ == "__main__":
    generate_mumbai_dataset()
