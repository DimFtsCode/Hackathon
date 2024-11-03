import requests

# Σωστό API URL για το Copernicus Data Space Ecosystem
api_url = "https://services.sentinel-hub.com/api/v1/ogc/wfs/"

# Παράμετροι για την περιοχή της Αθήνας (bounding box γύρω από την Αθήνα)
params = {
    'SERVICE': 'WFS',
    'VERSION': '2.0.0',
    'REQUEST': 'GetFeature',
    'TYPENAMES': 'urban_atlas:GreenUrbanArea',  # Παράδειγμα τύπου χαρακτηριστικού
    'SRSNAME': 'EPSG:4326',
    'BBOX': '23.664,37.841,23.781,38.080',  # Συντεταγμένες bounding box
    'OUTPUTFORMAT': 'application/json'
}

# API κλήση (χρησιμοποίησε το API key αν απαιτείται)
headers = {
    'Authorization': 'Bearer YOUR_API_KEY'  # Αντικατάστησε με το κλειδί API σου
}

try:
    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()  # Έλεγχος για τυχόν σφάλματα στην απόκριση
    data = response.json()
    
    # Επεξεργασία των δεδομένων και εμφάνιση
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
