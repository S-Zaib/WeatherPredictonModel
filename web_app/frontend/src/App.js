import React, { useState } from 'react';
import axios from 'axios';

const WeatherPredictionApp = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
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

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', { username, password });
      localStorage.setItem('token', response.data.token);
      setIsLoggedIn(true);
      setError(null);
    } catch (err) {
      setError('Login failed');
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/signup', { username, password });
      alert('Signup successful! Please login.');
    } catch (err) {
      setError('Signup failed');
    }
  };

  const handlePrediction = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/predict', predictionInput, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      setPrediction(response.data.temperature);
      setError(null);
    } catch (err) {
      setError('Prediction failed');
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
      <div>
        <h2>Login/Signup</h2>
        {error && <p style={{color: 'red'}}>{error}</p>}
        <form>
          <input 
            type="text" 
            placeholder="Username" 
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <input 
            type="password" 
            placeholder="Password" 
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <button onClick={handleLogin}>Login</button>
          <button onClick={handleSignup}>Signup</button>
        </form>
      </div>
    );
  }

  return (
    <div>
      <h2>Weather Temperature Prediction</h2>
      {error && <p style={{color: 'red'}}>{error}</p>}
      {prediction !== null && <p>Predicted Temperature: {prediction}°C</p>}
      <form onSubmit={handlePrediction}>
        {Object.keys(predictionInput).map((key) => (
          <input
            key={key}
            type="number"
            name={key}
            placeholder={key.replace('_', ' ').toUpperCase()}
            value={predictionInput[key]}
            onChange={handleInputChange}
          />
        ))}
        <button type="submit">Predict Temperature</button>
      </form>
    </div>
  );
};

export default WeatherPredictionApp;