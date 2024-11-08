import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# File paths and coordinates
weather_file = '/Users/giorgosziakas/Desktop/_weather_data.csv' # Το αρχείο που περιέχει τα δεδομένα καιρού
fire_file = '/Users/giorgosziakas/Desktop/Fire_dataset.csv'
region_center = (38.153, 23.963) # Κέντρο της περιοχής που θέλουμε να εξετάσουμε
fixed_radius_km = 2.46 # Σταθερή ακτίνα σε χιλιόμετρα

# Wind direction mapping
wind_translation = [("N", 360), ("S", 180), ("E", 90), ("W", 270), 
                    ("NW", 315), ("NE", 45), ("SE", 135), ("SW", 225),
                    ("WNW", 315), ("WSW", 45), ("NNW", 335), ("NNE", 25),
                    ("ENE", 65), ("ESE", 115), ("SSE", 155), ("SSW", 205)]

# Load data
def load_data(weather_file, fire_file):
    weather_data = pd.read_csv(weather_file)
    fire_data = pd.read_csv(fire_file)
    weather_data['date'] = pd.to_datetime(weather_data['date'])
    fire_data['acq_date'] = pd.to_datetime(fire_data['acq_date'])
    return weather_data, fire_data

# Haversine distance calculation
def haversine_distance(coord1, coord2):
    R = 6371.0
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# Add fire column with fixed radius
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

# Apply wind direction transformation
def apply_wind_translation(weather_data):
    for val in wind_translation:
        weather_data.replace(val[0], val[1], inplace=True)
    return weather_data

# Process region with fixed radius and apply transformation
def process_single_region_fixed_radius(weather_file, fire_file, region_center, fixed_radius_km):
    weather_data, fire_data = load_data(weather_file, fire_file)
    enriched_weather_data = add_fire_column_fixed_radius(weather_data, fire_data, region_center, fixed_radius_km)
    enriched_weather_data = apply_wind_translation(enriched_weather_data)  # Apply the wind translation here
    return enriched_weather_data

# Fire statistics calculation
def fire_statistics(fire_data, start_year, end_year):
    fire_data_period = fire_data[(fire_data['acq_date'].dt.year >= start_year) & (fire_data['acq_date'].dt.year <= end_year)]
    total_fire_days = fire_data_period['acq_date'].nunique()
    total_fires = len(fire_data_period)
    return total_fire_days, total_fires    






# Υπολογισμός συνολικών ημερών φωτιάς και αριθμού φωτιών
def fire_statistics(fire_data, start_year, end_year):
    """
    Υπολογίζει τον συνολικό αριθμό ημερών φωτιάς και τον συνολικό αριθμό φωτιών.
    """
    fire_data_period = fire_data[(fire_data['acq_date'].dt.year >= start_year) & (fire_data['acq_date'].dt.year <= end_year)]
    total_fire_days = fire_data_period['acq_date'].nunique()
    total_fires = len(fire_data_period)
    return total_fire_days, total_fires    


# Φόρτωση δεδομένων και υπολογισμός στατιστικών φωτιάς πριν από την επεξεργασία
weather_data, fire_data = load_data(weather_file, fire_file)


# Εκτέλεση της ανάλυσης για την περιοχή  με σταθερή ακτίνα
enriched_data = process_single_region_fixed_radius(weather_file, fire_file, region_center, fixed_radius_km)

# Αποθήκευση του εμπλουτισμένου συνόλου δεδομένων 
enriched_data.to_csv('/Users/giorgosziakas/Desktop/RegionName_final_dataset.csv', index=False)
