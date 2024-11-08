import pandas as pd 
from math import radians, sin, cos, sqrt, atan2

fire_file = "C:\Users\thoma\Documents\Hackathon\GiorgosScripts\Fire_Dataset\fire.csv"
weather_file = "C:\Users\thoma\Documents\Hackathon\DimiScripts\Datasets\Anthousa_weather_data.csv"

# Συναρτήσεις για φόρτωση δεδομένων και υπολογισμό απόστασης
def load_data(weather_file, fire_file):
    """
    Φορτώνει τα δεδομένα καιρού και φωτιάς από αρχεία.
    """
    weather_data = pd.read_csv(weather_file)
    fire_data = pd.read_csv(fire_file)
    weather_data['date'] = pd.to_datetime(weather_data['date'])
    fire_data['acq_date'] = pd.to_datetime(fire_data['acq_date'])
    return weather_data, fire_data

weather_data, fire_data = load_data(weather_file, fire_file)