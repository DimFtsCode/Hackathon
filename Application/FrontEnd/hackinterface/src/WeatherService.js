import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

// Λειτουργία για ανάκτηση όλων των δεδομένων καιρού
export const getAllWeatherData = async () => {
try {
    const response = await axios.get(`${API_URL}/weather/6730beff59469079dacf3c97`);
    console.log("Response from API:", response); // Προσθέστε αυτό για debugging
    return response.data;
    } catch (error) {
    console.error("Error fetching weather data by ID:", error);
    throw error;
    }
};
