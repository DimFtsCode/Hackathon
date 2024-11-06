from penteli import Penteli
from parnitha import Parnitha
from hymettus import Hymettus
from weatherfetcher import WeatherFetcher
import time

class MountainRegionsManager:
    def __init__(self, api_key):
        """
        Αρχικοποίηση των βουνών (Πεντέλη, Πάρνηθα, Υμηττός) και του WeatherFetcher.
        :param api_key: Το API key για το Weatherstack API.
        """
        self.penteli = Penteli()
        self.parnitha = Parnitha()
        self.hymettus = Hymettus()
        self.weather_fetcher = WeatherFetcher(api_key)
        self.mountains = {
            "Penteli": self.penteli,
            "Parnitha": self.parnitha,
            "Hymettus": self.hymettus
        }

    def display_regions_info(self):
        """
        Εμφανίζει τις περιοχές και τα εμβαδά τους για κάθε βουνό.
        """
        for mountain_name, mountain in self.mountains.items():
            print(f"\n{mountain_name} Regions:")
            print(mountain)
            for region in mountain.regions:
                print(f"Area of {region.name} region in {mountain_name}: {region.area_in_square_km():.2f} square kilometers")

    def check_point_in_mountains(self, point):
        """
        Ελέγχει αν ένα σημείο ανήκει σε κάποια από τις περιοχές των βουνών.
        :param point: Συντεταγμένες του σημείου (latitude, longitude).
        """
        for mountain_name, mountain in self.mountains.items():
            print(f"\nChecking point in {mountain_name}: {point}")
            result = mountain.find_region(point)
            print(result)

    def fetch_weather_for_all_regions(self):
        """
        Κάνει αίτημα στο Weatherstack API για να λάβει τα καιρικά δεδομένα για κάθε περιοχή σε όλα τα βουνά
        και τα αποθηκεύει σε αρχεία JSON.
        """
        for mountain_name, mountain in self.mountains.items():
            for region in mountain.regions:
                latitude, longitude = region.center
                print(f"latitude = {latitude} , longitute = {longitude}")
                self.weather_fetcher.fetch_weather(latitude, longitude, f"{mountain_name}_{region.name}")
                time.sleep(1)  # Καθυστέρηση 1 δευτερόλεπτο μετά από κάθε αίτημα