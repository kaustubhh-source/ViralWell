import os
import requests
import pandas as pd

def fetch_historical_mumbai_weather():
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    # Configure API parameters for Mumbai (2021-01-01 to 2025-12-31)
    params = {
        "latitude": 19.0760,
        "longitude": 72.8777,
        "start_date": "2021-01-01",
        "end_date": "2025-12-31",
        "daily": "temperature_2m_max,relative_humidity_2m_mean,rain_sum",
        "timezone": "Asia/Kolkata"
    }
    
    print("Requesting historical weather archive data from Open-Meteo API...")
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"API Request Failed: HTTP status code {response.status_code}")
            print(f"Response Content: {response.text}")
            return
            
        data = response.json()
        
        # Check if daily data is present in response
        if "daily" not in data:
            print("Error: 'daily' key not found in API response JSON.")
            print(f"Response: {data}")
            return
            
        daily_data = data["daily"]
        
        # Extract variables
        dates = daily_data.get("time", [])
        temp_max = daily_data.get("temperature_2m_max", [])
        humidity_mean = daily_data.get("relative_humidity_2m_mean", [])
        rain_sum = daily_data.get("rain_sum", [])
        
        # Verify lists length compatibility
        if not (len(dates) == len(temp_max) == len(humidity_mean) == len(rain_sum)):
            print("Warning: Retrieved data columns have mismatched sizes.")
            
        # Parse into a clean pandas DataFrame
        df = pd.DataFrame({
            "Date": dates,
            "Max_Temperature_C": temp_max,
            "Mean_Humidity_Pct": humidity_mean,
            "Daily_Rain_mm": rain_sum
        })
        
        # Ensure output directory exists
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "historical_mumbai_weather.csv")
        
        # Export DataFrame cleanly as CSV
        df.to_csv(output_path, index=False)
        
        print("\n=== Data Fetch Success ===")
        print(f"Successfully downloaded: {len(df)} historical daily weather rows.")
        print(f"Date Range: {df['Date'].min()} to {df['Date'].max()}")
        print(f"File saved to: {output_path}")
        print("==========================\n")
        
    except requests.exceptions.Timeout:
        print("Error: The request timed out. Open-Meteo servers might be busy.")
    except requests.exceptions.RequestException as e:
        print(f"Error: Network exception occurred: {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}")

if __name__ == "__main__":
    fetch_historical_mumbai_weather()
