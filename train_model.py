import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import json
import mlflow
import mlflow.sklearn
import os

def train_temperature_model(input_file):
    # Start MLflow experiment
    mlflow.set_experiment("temperature_prediction_experiment")

    with mlflow.start_run():
        # Hyperparameters
        model_type = "RandomForestRegressor"
        n_estimators = 100
        max_depth = None  # Default: None
        random_state = 42

        # Log model type and hyperparameters
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_param("random_state", random_state)

        # Load data
        data = pd.read_csv(input_file)

        # Log dataset details
        mlflow.log_param("input_file", input_file)
        mlflow.log_metric("dataset_size", data.shape[0])

        # Take X, Y
        X = data[['humidity', 'wind_speed', 'weather_condition', 'day_of_week', 'month', 'hour', 'day']]
        y = data['temperature']

        # Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

        # Train
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state)
        model.fit(X_train, y_train)

        # Test
        y_pred = model.predict(X_test)

        # Eval
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Log evaluation metrics
        mlflow.log_metric("mean_absolute_error", mae)
        mlflow.log_metric("mean_squared_error", mse)
        mlflow.log_metric("r2_score", r2)

        # Ensure metrics directory exists
        os.makedirs('metrics', exist_ok=True)

        # Save metrics locally as JSON
        metrics = {
            'mean_squared_error': mse,
            'mean_absolute_error': mae,
            'r2_score': r2
        }
        with open('metrics/metrics.json', 'w') as f:
            json.dump(metrics, f)

        # Ensure model directory exists
        os.makedirs('model', exist_ok=True)

        # Save model using joblib
        model_path = 'model/temperature_model.pkl'
        joblib.dump(model, model_path)
        print(f"Model saved as '{model_path}' in the model folder")

        # Log the trained model to MLflow
        mlflow.sklearn.log_model(model, artifact_path="temperature_model", registered_model_name="TemperaturePredictionModel")

        # Log the metrics JSON file as an artifact
        mlflow.log_artifact('metrics/metrics.json', artifact_path="metrics")

        print("Model, metrics, and artifacts logged to MLflow")

if __name__ == "__main__":
    train_temperature_model('data/processed/processed_data.csv')
