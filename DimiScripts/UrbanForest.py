import requests

# Σωστό API URL για το Copernicus CLMS Urban Atlas
api_url = "https://land.copernicus.eu/rest/v1/urban-atlas"

# Παράμετροι για συγκεκριμένες συντεταγμένες (bounding box) κοντά στην Αθήνα
params = {
    'bbox': '23.664,37.841,23.781,38.080',  # Χρησιμοποίησε συντεταγμένες για την περιοχή της Αθήνας
    'format': 'json',
    'layers': 'green_urban_areas'  # Παράδειγμα επιλογής κατάλληλου layer για urban forests ή green areas
}

# API κλήση (με το API key αν απαιτείται)
try:
    response = requests.get(api_url, params=params)
    response.raise_for_status()  # Έλεγχος για τυχόν σφάλματα στην απόκριση
    data = response.json()
    
    # Επεξεργασία δεδομένων και εμφάνιση
    for feature in data.get('features', []):
        properties = feature.get('properties', {})
        geometry = feature.get('geometry', {})
        
        # Ανάκτηση ονόματος περιοχής και συντεταγμένων
        area_name = properties.get('name', 'No area name available')
        coordinates = geometry.get('coordinates', 'No coordinates available')
        
        print(f"Area: {area_name}")
        print(f"Coordinates: {coordinates}\n")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
