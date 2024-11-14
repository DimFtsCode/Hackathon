import React, { useState, useEffect } from 'react';
import { getAllWeatherData } from './WeatherService'; 

const WeatherList = () => {
    const [weatherData, setWeatherData] = useState(null);
    const [loading, setLoading] = useState(true);
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const data = await getAllWeatherData();
          console.log("Fetched weather data:", data); // Για έλεγχο της δομής
          setWeatherData(data);
          setLoading(false);
        } catch (error) {
          console.error("Error fetching weather data:", error);
          setLoading(false);
        }
      };
  
      fetchData();
    }, []);
  
    if (loading) {
      return <p>Loading...</p>;
    }

    if (!weatherData) {
      return <p>No weather data available.</p>;
    }
  
    return (
      <div>
        <h1>Weather Data</h1>
        <ul>
          <li><strong>Name:</strong> {weatherData.name}</li>
          <li><strong>Temperature:</strong> {weatherData.temperature}°C</li>
          <li><strong>Humidity:</strong> {weatherData.humidity}%</li>
          <li><strong>Latitude:</strong> {weatherData.latitude}</li>
          <li><strong>Longitude:</strong> {weatherData.longitude}</li>
          <li><strong>Date:</strong> {weatherData.date}</li>
          <li><strong>Time:</strong> {weatherData.time}</li>
          <li><strong>Visibility:</strong> {weatherData.visibility}</li>
          <li><strong>Wind Direction:</strong> {weatherData.wind_dir}</li>
          <li><strong>Wind Speed:</strong> {weatherData.wind_speed}</li>
        </ul>
      </div>
    );
  };
  
export default WeatherList;
