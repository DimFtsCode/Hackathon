from RegionCycle import RegionCircle
from weatherfetcher import WeatherFetcher

class PenteliCycle:
    def __init__(self, api_key):
        # Όνομα της κύριας περιοχής
        self.name = "Penteli"
        self.weather_fetcher = WeatherFetcher(api_key, file_name="penteli_weather.json")
        
        # Ονόματα και συντεταγμένες των περιοχών
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
            ("Ntrafi", (38.024, 23.908))
        ]
        
        # Δημιουργία επιμέρους περιοχών
        self.regions = []
        for name, center in points:
            # Υπολογισμός απόστασης από το κοντινότερο σημείο
            min_distance = float('inf')
            for other_name, other_center in points:
                if center != other_center:
                    distance = RegionCircle(name, center, 0).haversine_distance(center, other_center)
                    if distance < min_distance:
                        min_distance = distance
                        
            # Η ακτίνα της περιοχής είναι το ήμισυ της απόστασης προς το κοντινότερο σημείο
            radius_km = min_distance / 2
            self.regions.append(RegionCircle(name, center, radius_km))
        
    def list_regions(self):
        """
        Επιστρέφει μια λίστα με τα ονόματα, τις συντεταγμένες και την ακτίνα κάθε επιμέρους περιοχής.
        """
        return [(region.name, region.center, region.radius_km) for region in self.regions]

    def fetch_all_weather_data(self):
        """
        Ανακτά και αποθηκεύει τα καιρικά δεδομένα για κάθε περιοχή στην περιοχή Πεντέλη.
        """
        for region in self.regions:
            latitude, longitude = region.center
            self.weather_fetcher.fetch_weather(latitude, longitude, region.name)

    def __str__(self):
        region_descriptions = ", ".join([f"{region.name} (center: {region.center}, radius: {region.radius_km:.2f} km)" for region in self.regions])
        return f"{self.name} Region includes: {region_descriptions}"

# Δημιουργία αντικειμένου PenteliCycle και ανάκτηση καιρικών δεδομένων
api_key = "23ecd879f082445734dc2066bf821571"  # Αντικαταστήστε με το API key σας
penteli_cycle = PenteliCycle(api_key)
print(penteli_cycle)
penteli_cycle.fetch_all_weather_data()
print("Weather data has been fetched and saved.")
