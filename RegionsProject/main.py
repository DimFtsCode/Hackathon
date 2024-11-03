from mountainregionsmanager import MountainRegionsManager

# API key για το Weatherstack API
api_key = "7bb6dcf6dccc3e10945b5033fffc3e9d"

# Δημιουργία του MountainRegionsManager
manager = MountainRegionsManager(api_key)

# Εμφάνιση πληροφοριών για τις περιοχές και τα εμβαδά τους
manager.display_regions_info()

# Έλεγχος σημείου για το αν βρίσκεται εντός των καθορισμένων περιοχών
point = (38.0700, 23.8900)  # Σημείο για έλεγχο
manager.check_point_in_mountains(point)

# Έλεγχος σημείου εκτός των καθορισμένων περιοχών
point_outside = (38.5000, 23.5000)
manager.check_point_in_mountains(point_outside)

# Απόκτηση καιρικών δεδομένων για όλες τις περιοχές και αποθήκευση σε JSON αρχεία
manager.fetch_weather_for_all_regions()
