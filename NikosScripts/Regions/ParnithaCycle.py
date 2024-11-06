from RegionCycle import RegionCircle
from weatherfetcher import WeatherFetcher

class ParnithaCycle:
    def __init__(self, api_key):
        # Όνομα της κύριας περιοχής
        self.name = "Parnitha"
        self.weather_fetcher = WeatherFetcher(api_key, file_name="parnitha_weather.json")
        
        # Ονόματα και συντεταγμένες των περιοχών
        points = [
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
parnitha_cycle = ParnithaCycle(api_key)
print(parnitha_cycle)
parnitha_cycle.fetch_all_weather_data()
print("Weather data has been fetched and saved.")
