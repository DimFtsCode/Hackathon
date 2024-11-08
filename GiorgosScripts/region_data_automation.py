import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import os

# Η λίστα με τις περιοχές σας, με τα κέντρα και τις ακτίνες τους
regions_data = [
    {"name": "Anthousa", "center": (38.025, 23.876), "radius": 1.40},
    {"name": "Melissia", "center": (38.05, 23.833), "radius": 0.90},
    {"name": "Vrilissia", "center": (38.034, 23.83), "radius": 0.90},
    {"name": "Kifisia", "center": (38.074, 23.811), "radius": 1.47},
    {"name": "Nea Erythraia", "center": (38.1, 23.817), "radius": 1.18},
    {"name": "Ekali", "center": (38.117, 23.833), "radius": 1.18},
    {"name": "Rapentosa", "center": (38.093, 23.904), "radius": 1.70},
    {"name": "Aigeirouses", "center": (38.07, 23.159), "radius": 28.54},
    {"name": "Rodopoli", "center": (38.117, 23.88), "radius": 1.70},
    {"name": "Vothon", "center": (38.17, 23.883), "radius": 2.95},
    {"name": "Grammatiko", "center": (38.203, 23.965), "radius": 2.78},
    {"name": "Kato Soulion", "center": (38.168, 24.016), "radius": 2.46},
    {"name": "Marathonas", "center": (38.153, 23.963), "radius": 2.46},
    {"name": "Ntaou Penteli", "center": (38.041, 23.945), "radius": 1.01},
    {"name": "Dioni", "center": (38.023, 23.933), "radius": 1.10},
    {"name": "Kallitechnoupoli", "center": (38.026, 23.958), "radius": 1.01},
    {"name": "Ntrafi", "center": (38.024, 23.908), "radius": 1.10}
]

# Διαδρομή προς τον κατάλογο που περιέχει τα αρχεία δεδομένων καιρού
weather_data_dir = '/Users/giorgosziakas/Desktop/WeatherData'

# Διαδρομή προς το αρχείο δεδομένων πυρκαγιών
fire_file = '/Users/giorgosziakas/Desktop/Fire_dataset.csv'

# Κατάλογος εξόδου για τα εμπλουτισμένα δεδομένα
output_dir = '/Users/giorgosziakas/Desktop/EnrichedData'

# Χαρτογράφηση κατεύθυνσης ανέμου
wind_translation = [
    ("N", 360), ("S", 180), ("E", 90), ("W", 270),
    ("NW", 315), ("NE", 45), ("SE", 135), ("SW", 225),
    ("WNW", 315), ("WSW", 45), ("NNW", 335), ("NNE", 25),
    ("ENE", 65), ("ESE", 115), ("SSE", 155), ("SSW", 205)
]

# Φόρτωση δεδομένων
def load_data(weather_file, fire_file):
    weather_data = pd.read_csv(weather_file)
    fire_data = pd.read_csv(fire_file)
    weather_data['date'] = pd.to_datetime(weather_data['date'])
    fire_data['acq_date'] = pd.to_datetime(fire_data['acq_date'])
    return weather_data, fire_data

# Υπολογισμός απόστασης Haversine
def haversine_distance(coord1, coord2):
    R = 6371.0  # Ακτίνα της Γης σε χιλιόμετρα
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# Προσθήκη στήλης "fire" με σταθερή ακτίνα
def add_fire_column_fixed_radius(weather_data, fire_data, region_center, fixed_radius_km):
    weather_data['fire'] = 0
    region_dates = set(weather_data['date'].unique()).intersection(fire_data['acq_date'].unique())
    for date in region_dates:
        fires_on_date = fire_data[fire_data['acq_date'] == date]
        for _, fire_row in fires_on_date.iterrows():
            fire_coords = fire_row['latitude'], fire_row['longitude']
            distance = haversine_distance(region_center, fire_coords)
            if distance <= fixed_radius_km:
                weather_data.loc[weather_data['date'] == date, 'fire'] = 1
                break
    return weather_data

# Εφαρμογή μετατροπής κατεύθυνσης ανέμου
def apply_wind_translation(weather_data):
    for val in wind_translation:
        weather_data.replace(val[0], val[1], inplace=True)
    return weather_data

# Επεξεργασία περιοχής με σταθερή ακτίνα και εφαρμογή μετασχηματισμού
def process_single_region_fixed_radius(weather_file, fire_file, region_center, fixed_radius_km):
    weather_data, fire_data = load_data(weather_file, fire_file)
    enriched_weather_data = add_fire_column_fixed_radius(weather_data, fire_data, region_center, fixed_radius_km)
    enriched_weather_data = apply_wind_translation(enriched_weather_data)
    return enriched_weather_data

# Δημιουργία καταλόγου εξόδου αν δεν υπάρχει
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Βρόχος για κάθε περιοχή και επεξεργασία
for region in regions_data:
    region_name = region['name']
    region_center = region['center']
    fixed_radius_km = region['radius']
    
    # Κατασκευή διαδρομής αρχείου δεδομένων καιρού
    weather_file = os.path.join(weather_data_dir, f"{region_name}_weather_data.csv")
    
    # Έλεγχος αν το αρχείο δεδομένων καιρού υπάρχει
    if not os.path.isfile(weather_file):
        print(f"Το αρχείο δεδομένων καιρού για την περιοχή {region_name} δεν βρέθηκε στο {weather_file}. Παράλειψη αυτής της περιοχής.")
        continue
    
    print(f"Επεξεργασία περιοχής: {region_name}")
    
    # Επεξεργασία της περιοχής
    enriched_data = process_single_region_fixed_radius(weather_file, fire_file, region_center, fixed_radius_km)
    
    # Κατασκευή διαδρομής αρχείου εξόδου
    output_file = os.path.join(output_dir, f"{region_name}_final_dataset.csv")
    
    # Αποθήκευση των εμπλουτισμένων δεδομένων
    enriched_data.to_csv(output_file, index=False)
    print(f"Τα εμπλουτισμένα δεδομένα για την περιοχή {region_name} αποθηκεύτηκαν στο {output_file}\n")
