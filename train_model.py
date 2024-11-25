import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import joblib


def train_temperature_model(input_file):
    # Load data
    data = pd.read_csv(input_file)

    # Take X, Y (predicting temp based on other features)
    X = data[['humidity', 'wind_speed', 'weather_condition', 'day_of_week', 'month', 'hour', 'day']]
    y = data['temperature']

    # Split the data 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Test
    y_pred = model.predict(X_test)

    # Evaluate the model
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.4f}")

    # Save the trained model
    joblib.dump(model, 'temperature_model.pkl')
    print("Model saved as 'temperature_model.pkl'")


if __name__ == "__main__":
    train_temperature_model('data/processed/processed_data.csv')
