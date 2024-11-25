import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import os

def preprocess_weather_data(input_path, output_path):
    """Preprocess the weather data."""
    # Load the raw data
    df = pd.read_csv(input_path)

    # Handle missing values
    df['temperature'].fillna(df['temperature'].mean(), inplace=True)
    df['humidity'].fillna(df['humidity'].mean(), inplace=True)
    df['wind_speed'].fillna(df['wind_speed'].mean(), inplace=True)
    df.dropna(subset=['date_time', 'weather_condition'], inplace=True)

    # Normalize numerical columns
    scaler = MinMaxScaler()
    df[['temperature', 'humidity', 'wind_speed']] = scaler.fit_transform(
        df[['temperature', 'humidity', 'wind_speed']]
    )

    # Map weather conditions to categories (grouping similar conditions)
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
    
    # Apply the mapping to encode weather conditions
    df['weather_condition_encoded'] = df['weather_condition'].map(weather_mapping)

    # Ensure all weather conditions are accounted for
    if df['weather_condition_encoded'].isnull().any():
        missing_conditions = df[df['weather_condition_encoded'].isnull()]['weather_condition'].unique()
        print(f"Warning: Unmapped weather conditions found: {missing_conditions}")
        df['weather_condition_encoded'].fillna(-1, inplace=True)  # Assign -1 for unmapped conditions


    # Save the processed data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")


if __name__ == "__main__":
    # Paths
    raw_data_path = "data/raw/raw.csv"  
    processed_data_path = "data/processed/processed_data.csv"  

    # Preprocess the data
    preprocess_weather_data(raw_data_path, processed_data_path)
