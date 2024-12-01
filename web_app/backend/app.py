import os
import sys
import joblib
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import numpy as np

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

app = Flask(__name__)
CORS(app)

# load the model
MODEL_PATH = os.path.join(project_root, 'model', 'temperature_model.pkl')
with open(MODEL_PATH, 'rb') as file:
    model = joblib.load(file)

def init_db():
    conn = sqlite3.connect(os.path.join(project_root, 'web_app', 'backend', 'users.db'))
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            user_id INTEGER,
            token TEXT UNIQUE NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db_connection():
    return sqlite3.connect(os.path.join(project_root, 'web_app', 'backend', 'users.db'))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = get_db_connection()
    try:
        c = conn.cursor()
        hashed_password = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                  (username, hashed_password))
        conn.commit()
        return jsonify({"message": "User created successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password_hash(user[2], password):
        token = os.urandom(16).hex()
        
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO sessions (user_id, token) VALUES (?, ?)", 
                  (user[0], token))
        conn.commit()
        conn.close()

        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Extract features in the same order as training
    features = [
        data.get('humidity'),
        data.get('wind_speed'),
        data.get('weather_condition'),
        data.get('day_of_week'),
        data.get('month'),
        data.get('hour'),
        data.get('day')
    ]

    # Validate all features are present
    if None in features:
        return jsonify({"error": "Missing required features"}), 400

    # Reshape for prediction
    features_array = np.array(features).reshape(1, -1)
    
    try:
        prediction = model.predict(features_array)[0]
        return jsonify({"temperature": float(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)