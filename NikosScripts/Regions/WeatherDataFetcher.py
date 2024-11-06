import requests
import csv
import os

class WeatherDataFetcher:
    def __init__(self, api_key, latitude, longitude, start_date, end_date):
        """
        Αρχικοποίηση της κλάσης με το API key και τα δεδομένα τοποθεσίας και ημερομηνιών.
        
        :param api_key: Το API key για το Weatherstack.
        :param latitude: Το γεωγραφικό πλάτος της περιοχής.
        :param longitude: Το γεωγραφικό μήκος της περιοχής.
        :param start_date: Η αρχική ημερομηνία σε μορφή 'YYYY-MM-DD'.
        :param end_date: Η τελική ημερομηνία σε μορφή 'YYYY-MM-DD'.
        """
        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.base_url = "http://api.weatherstack.com/historical"
    
    def fetch_and_save(self, output_file="weather_data.csv"):
        """
        Ανακτά ιστορικά δεδομένα καιρού από το API και τα προσθέτει στο τέλος του αρχείου CSV.
        
        :param output_file: Το όνομα του αρχείου CSV για την αποθήκευση των δεδομένων.
        """
        url = f"{self.base_url}?access_key={self.api_key}&query={self.latitude},{self.longitude}&historical_date_start={self.start_date}&historical_date_end={self.end_date}&hourly=1"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Έλεγχος αν το αίτημα ολοκληρώθηκε επιτυχώς
            data = response.json()

            # Έλεγχος αν το API επέστρεψε σωστά δεδομένα
            if 'error' in data:
                print(f"Error fetching data: {data['error']['info']}")
                return
            
            historical_data = data.get("historical", {})

            # Άνοιγμα του αρχείου σε λειτουργία προσθήκης ('a')
            file_exists = os.path.isfile(output_file)
            with open(output_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                
                # Προσθήκη επικεφαλίδας μόνο αν το αρχείο δεν υπάρχει ήδη
                if not file_exists:
                    header = ["name", "latitude", "longitude", "date", "time", "temperature", 
                              "wind_speed", "wind_dir", 
                              "humidity", "visibility"]
                    writer.writerow(header)

                # Επεξεργασία δεδομένων για κάθε ημέρα και ώρα
                for date, day_data in historical_data.items():
                    hourly_data = day_data.get("hourly", [])
                    for hour_data in hourly_data:
                        row = [
                            data.get("location", {}).get("name", "N/A"),
                            self.latitude,
                            self.longitude,
                            date,
                            hour_data.get("time", "N/A"),
                            hour_data.get("temperature", "N/A"),
                            hour_data.get("wind_speed", "N/A"),
                            # hour_data.get("wind_degree", "N/A"),
                            hour_data.get("wind_dir", "N/A"),
                            # hour_data.get("pressure", "N/A"),
                            # hour_data.get("precip", "N/A"),
                            hour_data.get("humidity", "N/A"),
                            # hour_data.get("cloudcover", "N/A"),
                            # hour_data.get("feelslike", "N/A"),
                            # hour_data.get("uv_index", "N/A"),
                            hour_data.get("visibility", "N/A"),
                            # hour_data.get("is_day", "N/A")
                        ]
                        writer.writerow(row)
            
            print(f"Weather data has been added to {output_file}.")
        
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            

