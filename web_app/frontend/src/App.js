import React, { useState } from 'react';
import axios from 'axios';

const WeatherPredictionApp = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loggedInUser, setLoggedInUser] = useState(null); // To store the username of the logged-in user
  const [predictionInput, setPredictionInput] = useState({
    humidity: '',
    wind_speed: '',
    weather_condition: '',
    day_of_week: '',
    month: '',
    hour: '',
    day: ''
  });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const weatherMapping = {
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
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please fill in all fields for login.');
      return;
    }
    try {
      const response = await axios.post('http://localhost:5000/login', { username, password });
      localStorage.setItem('token', response.data.token);
      setLoggedInUser(response.data.username);
      setIsLoggedIn(true);
      setError(null);
    } catch (err) {
      setError('Login failed.');
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please fill in all fields for signup.');
      return;
    }
    try {
      await axios.post('http://localhost:5000/signup', { username, password });
      alert('Signup successful! Please login.');
      setError(null);
    } catch (err) {
      setError('Signup failed.');
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post('http://localhost:5000/logout', {}, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      localStorage.removeItem('token');
      setIsLoggedIn(false);
      setLoggedInUser(null);
      setError(null);
    } catch (err) {
      setError('Logout failed.');
    }
  };

  const handleDeleteAccount = async () => {
    const confirmDelete = window.confirm("Are you sure you want to delete your account?");
    if (!confirmDelete) return;

    try {
      await axios.delete('http://localhost:5000/delete_account', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      localStorage.removeItem('token');
      setIsLoggedIn(false);
      setLoggedInUser(null);
      alert('Account deleted successfully.');
    } catch (err) {
      setError('Failed to delete account.');
    }
  };

  const handlePrediction = async (e) => {
    e.preventDefault();
    const hasEmptyFields = Object.values(predictionInput).some((value) => value === '');
    if (hasEmptyFields) {
      setError('Please fill in all prediction fields.');
      return;
    }
    try {
      const mappedInput = {
        ...predictionInput,
        weather_condition: weatherMapping[predictionInput.weather_condition] ?? -1
      };
      const response = await axios.post('http://localhost:5000/predict', mappedInput, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      setPrediction(response.data.temperature);
      setError(null);
    } catch (err) {
      setError('Prediction failed.');
    }
  };

  const handleInputChange = (e) => {
    setPredictionInput({
      ...predictionInput,
      [e.target.name]: e.target.value
    });
  };

  if (!isLoggedIn) {
    return (
      <div style={styles.container}>
        <h2>Login/Signup</h2>
        {error && <p style={styles.error}>{error}</p>}
        <form style={styles.form}>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={styles.input}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
          />
          <button onClick={handleLogin} style={styles.button}>Login</button>
          <button onClick={handleSignup} style={styles.button}>Signup</button>
        </form>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h2>Weather Temperature Prediction</h2>
      <p>Logged in as: <strong>{loggedInUser}</strong></p>
      <button onClick={handleLogout} style={styles.buttonSecondary}>Logout</button>
      <button onClick={handleDeleteAccount} style={styles.buttonDanger}>Delete Account</button>
      {error && <p style={styles.error}>{error}</p>}
      {prediction !== null && <p style={styles.prediction}>Predicted Temperature: {prediction}°C</p>}
      <form onSubmit={handlePrediction} style={styles.form}>
        {Object.keys(predictionInput).map((key) => (
          key === "weather_condition" ? (
            <select
              key={key}
              name={key}
              value={predictionInput[key]}
              onChange={handleInputChange}
              style={styles.input}
            >
              <option value="">Select Weather Condition</option>
              {Object.keys(weatherMapping).map((condition) => (
                <option key={condition} value={condition}>
                  {condition}
                </option>
              ))}
            </select>
          ) : (
            <input
              key={key}
              type="number"
              name={key}
              placeholder={key.replace('_', ' ').toUpperCase()}
              value={predictionInput[key]}
              onChange={handleInputChange}
              style={styles.input}
            />
          )
        ))}
        <button type="submit" style={styles.button}>Predict Temperature</button>
      </form>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '400px',
    margin: 'auto',
    textAlign: 'center',
    fontFamily: 'Arial, sans-serif',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#f9f9f9'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    margin: '20px 0'
  },
  input: {
    padding: '10px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px'
  },
  button: {
    padding: '10px',
    fontSize: '16px',
    color: '#fff',
    backgroundColor: '#007BFF',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  buttonSecondary: {
    padding: '10px',
    fontSize: '16px',
    color: '#fff',
    backgroundColor: '#6c757d',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginRight: '10px'
  },
  buttonDanger: {
    padding: '10px',
    fontSize: '16px',
    color: '#fff',
    backgroundColor: '#dc3545',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  error: {
    color: 'red',
    marginBottom: '10px'
  },
  prediction: {
    color: 'green',
    fontWeight: 'bold',
    margin: '20px 0'
  }
};

export default WeatherPredictionApp;
