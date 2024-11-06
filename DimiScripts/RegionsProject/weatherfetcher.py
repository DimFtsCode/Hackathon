import requests
import json
import os

class WeatherFetcher:
    def __init__(self, api_key, file_name="weather_data.json"):
        """
        Αρχικοποίηση της κλάσης με το API key και το όνομα του αρχείου αποθήκευσης.
        
        :param api_key: Το API key για πρόσβαση στο Weatherstack API.
        :param file_name: Το όνομα του αρχείου στο οποίο θα αποθηκεύονται τα δεδομένα.
        """
        self.api_key = api_key
        self.base_url = "http://api.weatherstack.com/current"
        self.file_name = file_name

    def fetch_weather(self, latitude, longitude, region_name):
        """
        Κάνει αίτημα στο Weatherstack API για να λάβει τα τρέχοντα καιρικά δεδομένα για μια περιοχή
        και αποθηκεύει το αποτέλεσμα σε ένα αρχείο JSON με τη μορφή dictionary.

        :param latitude: Το γεωγραφικό πλάτος της περιοχής.
        :param longitude: Το γεωγραφικό μήκος της περιοχής.
        :param region_name: Το όνομα της περιοχής (χρησιμοποιείται ως κλειδί στο dictionary).
        """
        # Εκτύπωση συντεταγμένων και επιβεβαίωση από τον χρήστη
        # print(f"\nLatitude: {latitude}, Longitude: {longitude}")
        # user_input = input(f"Do you want to fetch weather data for {region_name}? (yes/no): ").strip().lower()

        # # Αν ο χρήστης απαντήσει όχι, παραλείπουμε το αίτημα
        # if user_input != "yes":
        #     print(f"Skipping weather data fetch for {region_name}.")
        #     return

        url = f"{self.base_url}?access_key={self.api_key}&query={latitude},{longitude}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()  # Έλεγχος αν το αίτημα ολοκληρώθηκε επιτυχώς
            data = response.json()
            
            # Έλεγχος αν το API επέστρεψε σωστά δεδομένα
            if "current" in data:
                # Φορτώνουμε τα υπάρχοντα δεδομένα, αν υπάρχουν, από το αρχείο JSON
                if os.path.exists(self.file_name):
                    with open(self.file_name, 'r') as json_file:
                        all_data = json.load(json_file)
                else:
                    all_data = {}

                # Προσθήκη των νέων δεδομένων με το όνομα της περιοχής ως κλειδί
                all_data[region_name] = data

                # Αποθήκευση όλων των δεδομένων πίσω στο αρχείο JSON
                with open(self.file_name, 'w') as json_file:
                    json.dump(all_data, json_file, indent=4)
                
                print(f"Weather data for {region_name} saved to {self.file_name}.")
            else:
                print(f"Error fetching data for {region_name}: {data.get('error', {}).get('info', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
