from RegionCycle import RegionCycle
from datetime import datetime

class MountainsCycle:
    def __init__(self, api_key):
        self.name = "Mountains"
        self.api_key = api_key
        
        
        # Λίστα με τις περιοχές και τις συντεταγμένες τους
        points = [
            ("Anthousa", (38.025, 23.876)),
            ("Melissia", (38.050, 23.833)),
            ("Vrilissia", (38.034, 23.830)),
            ("Kifisia", (38.074, 23.811)),
            ("Nea Erythraia", (38.100, 23.817)),
            ("Ekali", (38.117, 23.833)),
            ("Rapentosa", (38.093, 23.904)),
            ("Aigeirouses", (38.070, 23.159)),
            ("Rodopoli", (38.117, 23.88)),
            ("Vothon", (38.17, 23.883)),
            ("Grammatiko", (38.203, 23.965)),
            ("Kato Soulion", (38.168, 24.016)),
            ("Marathonas", (38.153, 23.963)),
            ("Ntaou Penteli", (38.041, 23.945)),
            ("Dioni", (38.023, 23.933)),
            ("Kallitechnoupoli", (38.026, 23.958)),
            ("Ntrafi", (38.024, 23.908)),
            ("Parnis", (38.15, 23.74)),
            ("Acharnes", (38.08, 23.73)),
            ("Ano Liosia", (38.08, 23.70)),
            ("Fyli", (38.10, 23.66)),
            ("Aspropyrgos", (38.06, 23.59)),
            ("Skourta", (38.21, 23.55)),
            ("Moni Osiou Meletiou", (38.19, 23.45)),  #Dervenoxwria
            ("Avlonas", (38.25, 23.69)),
            ("Varympompi", (38.12, 23.78)),
            ("Afidnes", (38.20, 23.84)),
            ("Agia Triada", (38.20, 23.79)), #Ippokrateios Politeia
            ("Malakasa", (38.23, 23.80))
        ]
        
        # Δημιουργία των περιοχών ως αντικείμενα `RegionCycle`
        self.regions = []
        for name, center in points:
            min_distance = float('inf')
            for other_name, other_center in points:
                if center != other_center:
                    # Εδώ δημιουργούμε ένα προσωρινό αντικείμενο RegionCycle για υπολογισμό απόστασης χωρίς να αποθηκεύουμε δεδομένα
                    temp_region = RegionCycle(name, center, 0, api_key=self.api_key)
                    distance = temp_region.haversine_distance(center, other_center)
                    if distance < min_distance:
                        min_distance = distance
            radius_km = min_distance / 2
            # Δημιουργούμε και προσθέτουμε το RegionCycle με το σωστό API key και συλλογή MongoDB
            self.regions.append(RegionCycle(name, center, radius_km, api_key=self.api_key))

    def fetch_all_weather_data(self):
        """
        Καλεί την `fetch_weather` για κάθε περιοχή, συλλέγει τα δεδομένα και τα επεξεργάζεται ή τα αποθηκεύει στη MongoDB.
        """
        all_weather_data = []

        for region in self.regions:
            weather_data = region.fetch_weather()  # Ανάκτηση των δεδομένων χωρίς αποθήκευση στη MongoDB από το RegionCycle
            if weather_data:
                all_weather_data.append(weather_data)

        print(f"[{datetime.now()}] Weather data for all regions has been collected and saved to MongoDB.")

        return all_weather_data 
