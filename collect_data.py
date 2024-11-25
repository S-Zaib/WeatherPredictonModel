import requests
import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

def collect_weather_data():
    """Collect hourly weather data for every hour of the past 5 days for Islamabad"""
    API_KEY = os.getenv('OPENWEATHER_API_KEY')
    
    # Coordinates for Islamabad
    LAT = 33.6844
    LON = 73.0479
    
    base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"
    
    weather_data = []
    
    # Calculate timestamps for the past 5 days
    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Iterate through past 5 days
    for day_offset in range(5):
        current_day = end_date - timedelta(days=day_offset+1)
        
        # Generate timestamps for every hour of the day
        for hour in range(24):
            specific_hour = current_day + timedelta(hours=hour)
            timestamp = int(specific_hour.timestamp())
            
            params = {
                'lat': LAT,
                'lon': LON,
                'dt': timestamp,
                'appid': API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                
                # Extract data for this specific timestamp
                hourly_data = data.get('data', [{}])[0]
                
                if hourly_data:
                    weather_data.append({
                        'date_time': datetime.fromtimestamp(hourly_data['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                        'temperature': hourly_data['temp'],
                        'humidity': hourly_data['humidity'],
                        'wind_speed': hourly_data['wind_speed'],
                        'weather_condition': hourly_data['weather'][0]['main']
                    })
            else:
                print(f"Error fetching data for {specific_hour}: Status code {response.status_code}")
    
    # Create DataFrame
    df = pd.DataFrame(weather_data)
    
    # Ensure data directory exists
    os.makedirs('data/raw', exist_ok=True)
    
    # Save to CSV
    output_path = 'data/raw/raw.csv'
    df.to_csv(output_path, index=False)
    
    return output_path

if __name__ == '__main__':
    collect_weather_data()