import requests
from datetime import datetime
from math import radians, sin, cos, sqrt, atan2

class RegionCycle:
    def __init__(self, name, center, radius_km, api_key):
        self.name = name
        self.center = center  # Center as (latitude, longitude)
        self.radius_km = radius_km  # Radius in kilometers
        self.api_key = api_key
        self.base_url = "http://api.weatherstack.com/current"

    def haversine_distance(self, coord1, coord2):
        """
        Υπολογίζει την απόσταση σε χιλιόμετρα μεταξύ δύο γεωγραφικών σημείων χρησιμοποιώντας τον τύπο Haversine.
        :param coord1: Συντεταγμένες (latitude, longitude) του πρώτου σημείου.
        :param coord2: Συντεταγμένες (latitude, longitude) του δεύτερου σημείου.
        :return: Η απόσταση σε χιλιόμετρα.
        """
        R = 6371.0  # Ακτίνα της Γης σε χιλιόμετρα

        lat1, lon1 = radians(coord1[0]), radians(coord1[1])
        lat2, lon2 = radians(coord2[0]), radians(coord2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def fetch_weather(self):
        """
        Κάνει αίτημα στο Weatherstack API και επιστρέφει τα δεδομένα καιρού και την ακτίνα ως dictionary.
        """
        latitude, longitude = self.center
        url = f"{self.base_url}?access_key={self.api_key}&query={latitude},{longitude}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if "current" in data:
                # Εξαγωγή των επιλεγμένων δεδομένων
                filtered_data = {
                    "name": self.name,
                    "latitude": latitude,
                    "longitude": longitude,
                    "radius_km": self.radius_km,  # Συμπεριλαμβάνει την ακτίνα
                    "date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "time": datetime.utcnow().strftime("%H:%M"),
                    "temperature": data["current"].get("temperature"),
                    "wind_speed": data["current"].get("wind_speed"),
                    "wind_dir": data["current"].get("wind_dir"),
                    "humidity": data["current"].get("humidity"),
                    "visibility": data["current"].get("visibility"),
                }

                return filtered_data  # Επιστρέφει τα δεδομένα αντί να τα αποθηκεύει
            else:
                print(f"Error fetching data for {self.name}: {data.get('error', {}).get('info', 'Unknown error')}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def is_within_region(self, point):
        """
        Ελέγχει αν το δεδομένο σημείο βρίσκεται εντός της κυκλικής περιοχής.
        :param point: Συντεταγμένες (latitude, longitude) του σημείου.
        :return: True αν το σημείο βρίσκεται εντός της περιοχής, αλλιώς False.
        """
        distance = self.haversine_distance(self.center, point)
        return distance <= self.radius_km

    def __str__(self):
        return f"{self.name} Circular Region with center at {self.center} and radius {self.radius_km} km"
