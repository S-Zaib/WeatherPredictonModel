import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json

def train_temperature_model(input_file):
    # Load data
    data = pd.read_csv(input_file)

    # Take X, Y
    X = data[['humidity', 'wind_speed', 'weather_condition', 'day_of_week', 'month', 'hour', 'day']]
    y = data['temperature']

    # Split 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Test
    y_pred = model.predict(X_test)

    # Eval
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Save metrics
    metrics = {
        'mean_squared_error': mse,
        'mean_absolute_error': mae,
        'r2_score': r2
    }

    with open('metrics/metrics.json', 'w') as f:
        json.dump(metrics, f)

    # Save
    joblib.dump(model, 'model/temperature_model.pkl')
    print("Model saved as 'temperature_model.pkl' in the model folder")


if __name__ == "__main__":
    train_temperature_model('data/processed/processed_data.csv')
