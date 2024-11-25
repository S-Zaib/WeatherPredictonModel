import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def collect_weather_data():
    """Collect 5 days of historical weather data for Islamabad using One Call API 3.0"""
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    # Coordinates for Islamabad
    LAT = 33.6844
    LON = 73.0479
    
    base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    
    weather_data = []
    current_time = int(datetime.now().timestamp())
    
    # Collect 5 days of historical data backwards
    for i in range(5):
        params = {
            'lat': LAT,
            'lon': LON,
            'dt': current_time - (i * 24 * 60 * 60),  # Go back one day at a time
            'appid': API_KEY,
            'units': 'metric'
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            
            # Extract hourly data for the day
            for hourly_data in data.get('data', []):
                weather_data.append({
                    'date_time': datetime.fromtimestamp(hourly_data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                    'temperature': hourly_data['temp'],
                    'humidity': hourly_data['humidity'],
                    'wind_speed': hourly_data['wind_speed'],
                    'weather_condition': hourly_data['weather'][0]['main']
                })
        else:
            print("balls", response)
    
    # Create DataFrame
    df = pd.DataFrame(weather_data)
    
    # Ensure data directory exists
    os.makedirs('data/raw', exist_ok=True)
    
    # Save to CSV
    output_path = 'data/raw/raw.csv'
    df.to_csv(output_path, index=False)
    
    return output_path

# Main execution for standalone script
if __name__ == '__main__':
    collect_weather_data()