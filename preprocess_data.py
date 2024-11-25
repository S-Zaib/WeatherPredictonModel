import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import numpy as np

# Function to preprocess the weather data
def preprocess_weather_data(file_path, output_path):
    
    # Load the data
    data = pd.read_csv(file_path)

    # Convert date_time to pandas format
    data['date_time'] = pd.to_datetime(data['date_time'])

    # Extract useful features from
    data['day_of_week'] = data['date_time'].dt.dayofweek  # Monday=0, Sunday=6
    data['month'] = data['date_time'].dt.month
    data['hour'] = data['date_time'].dt.hour
    data['day'] = data['date_time'].dt.day

    # missing values (if any)
    imputer = SimpleImputer(strategy='mean')  # For numerical columns
    data[['temperature', 'humidity', 'wind_speed']] = imputer.fit_transform(
        data[['temperature', 'humidity', 'wind_speed']]
    )
    
    # Map weather conditions, categorical encoding
    weather_mapping = {
        "Clear": 0,
        "Clouds": 1,
        "Rain": 2,
        "Drizzle": 2,
        "Thunderstorm": 3,
        "Snow": 4,
        "Mist": 5,
        "Smoke": 5,
        "Haze": 5,
        "Dust": 5,
        "Fog": 5,
        "Sand": 5,
        "Ash": 5,
        "Squall": 5,
        "Tornado": 5
    }
    
    # No need for scaling features since RandomForestRegressor doesnt need its features scaled :)

    # Apply the mapping to the weather_condition column
    data['weather_condition'] = data['weather_condition'].map(weather_mapping)

    # Drop the original date_time
    data = data.drop(columns=['date_time'])

    # Save the preprocessed data
    data.to_csv(output_path, index=False)
    print(f"Preprocessed data saved to {output_path}")


if __name__ == "__main__":
    preprocess_weather_data('data/raw/raw.csv', 'data/processed/processed_data.csv')
