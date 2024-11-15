import requests
from pymongo import MongoClient
from datetime import datetime

class WeatherFetcher:
    def __init__(self, api_key, collection):
        """
        Αρχικοποίηση της κλάσης με το API key και τη συλλογή MongoDB.
        
        :param api_key: Το API key για το Weatherstack API.
        :param collection: Η συλλογή MongoDB όπου θα αποθηκεύονται τα δεδομένα.
        """
        self.api_key = api_key
        self.base_url = "http://api.weatherstack.com/current"
        self.collection = collection

    def fetch_weather(self, latitude, longitude, region_name):
        """
        Κάνει αίτημα στο Weatherstack API και αποθηκεύει τα δεδομένα στη MongoDB.

        :param latitude: Το γεωγραφικό πλάτος της περιοχής.
        :param longitude: Το γεωγραφικό μήκος της περιοχής.
        :param region_name: Το όνομα της περιοχής.
        """
        url = f"{self.base_url}?access_key={self.api_key}&query={latitude},{longitude}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Έλεγχος αν υπάρχουν δεδομένα
            if "current" in data:
                # Εξαγωγή των επιλεγμένων δεδομένων
                filtered_data = {
                    "name": region_name,
                    "latitude": latitude,
                    "longitude": longitude,
                    "date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "time": datetime.utcnow().strftime("%H:%M"),
                    "temperature": data["current"].get("temperature"),
                    "wind_speed": data["current"].get("wind_speed"),
                    "wind_dir": data["current"].get("wind_dir"),
                    "humidity": data["current"].get("humidity"),
                    "visibility": data["current"].get("visibility"),
                }

                # Αποθήκευση στη MongoDB
                self.collection.insert_one(filtered_data)
                print(f"Filtered weather data for {region_name} saved to MongoDB.")
            else:
                print(f"Error fetching data for {region_name}: {data.get('error', {}).get('info', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
