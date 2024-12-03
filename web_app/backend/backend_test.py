import os
import sys
import pytest
import json
# Add the project root to the Python path to locate the `web_app` module
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

from web_app.backend.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_signup(client):
    signup_data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post('/signup', 
                           data=json.dumps(signup_data), 
                           content_type='application/json')
    assert response.status_code in [201, 409]  # 201 for success, 409 if user already exists

def test_login(client):
    # Ensure the user exists by signing up
    signup_data = {
        'username': 'loginuser',
        'password': 'loginpassword'
    }
    client.post('/signup', 
                data=json.dumps(signup_data), 
                content_type='application/json')
    
    # Test login
    login_data = {
        'username': 'loginuser',
        'password': 'loginpassword'
    }
    response = client.post('/login', 
                           data=json.dumps(login_data), 
                           content_type='application/json')
    assert response.status_code == 200
    assert 'token' in response.json
    return response.json['token']

def test_logout(client):
    # Login and get a token
    token = test_login(client)
    
    # Test logout
    response = client.post('/logout', 
                           headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == "Logged out successfully"

def test_predict(client):
    # Login and get a token
    token = test_login(client)
    
    # Simulate a prediction request
    predict_data = {
        'humidity': 50.0,
        'wind_speed': 5.0,
        'weather_condition': 1,  # 'Clouds' mapped to 1
        'day_of_week': 2,  # Tuesday
        'month': 8,  # August
        'hour': 12,  # Noon
        'day': 10
    }
    response = client.post('/predict', 
                           data=json.dumps(predict_data), 
                           content_type='application/json',
                           headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'temperature' in response.json

def test_delete_account(client):
    # Ensure the user exists by signing up
    signup_data = {
        'username': 'deletetestuser',
        'password': 'testpassword'
    }
    client.post('/signup', 
                data=json.dumps(signup_data), 
                content_type='application/json')
    
    # Login and get a token
    login_data = {
        'username': 'deletetestuser',
        'password': 'testpassword'
    }
    login_response = client.post('/login', 
                                 data=json.dumps(login_data), 
                                 content_type='application/json')
    token = login_response.json['token']
    
    # Test delete account
    response = client.delete('/delete_account', 
                             headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['message'] == "Account deleted successfully"
