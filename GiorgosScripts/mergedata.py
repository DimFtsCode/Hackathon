import pandas as pd
from math import radians, sin, cos, sqrt, atan2

# Ορισμός αρχείων δεδομένων και συντεταγμένων περιοχής
weather_file = '/Users/giorgosziakas/Desktop/Anthousa_weather_data.csv'
fire_file = '/Users/giorgosziakas/Desktop/3.csv'
region_center = (38.025, 23.876)  # Συντεταγμένες για την Ανθούσα
fixed_radius_km = 1.40  # Σταθερή ακτίνα για την Ανθούσα

# Συναρτήσεις για φόρτωση δεδομένων και υπολογισμό απόστασης
def load_data(weather_file, fire_file):
    """
    Φορτώνει τα δεδομένα καιρού και φωτιάς από αρχεία.
    """
    weather_data = pd.read_csv(weather_file)
    fire_data = pd.read_csv(fire_file)
    weather_data['date'] = pd.to_datetime(weather_data['date'])
    fire_data['acq_date'] = pd.to_datetime(fire_data['acq_date'])
    return weather_data, fire_data


def haversine_distance(coord1, coord2):
    """
    Υπολογίζει την απόσταση σε χιλιόμετρα μεταξύ δύο γεωγραφικών σημείων
    χρησιμοποιώντας τον τύπο Haversine.
    """
    R = 6371.0  # Ακτίνα της γης σε χιλιόμετρα
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# Συνάρτηση για προσθήκη στήλης με σταθερή ακτίνα
def add_fire_column_fixed_radius(weather_data, fire_data, region_center, fixed_radius_km):
    """
    Προσθέτει μια στήλη στα δεδομένα καιρού που δείχνει αν υπήρχε κοντινή φωτιά,
    χρησιμοποιώντας σταθερή ακτίνα.
    """
    weather_data['fire'] = 0  # Δημιουργία νέας στήλης για παρουσία φωτιάς

    # Εύρεση κοινών ημερομηνιών μεταξύ δεδομένων καιρού και φωτιάς
    region_dates = set(weather_data['date'].unique()).intersection(fire_data['acq_date'].unique())

    # Για κάθε κοινή ημερομηνία, έλεγχος για φωτιές εντός της σταθερής ακτίνας
    for date in region_dates:
        fires_on_date = fire_data[fire_data['acq_date'] == date]

        for _, fire_row in fires_on_date.iterrows():
            fire_coords = fire_row['latitude'], fire_row['longitude']
            distance = haversine_distance(region_center, fire_coords)
            if distance <= fixed_radius_km:
                # Αν υπάρχει φωτιά εντός της σταθερής ακτίνας, καταχώρηση '1' για την ημέρα
                weather_data.loc[weather_data['date'] == date, 'fire'] = 1
                break  # Σταματάμε τον έλεγχο αν βρεθεί κοντινή φωτιά
            
    return weather_data


# Διαδικασία για μία περιοχή με σταθερή ακτίνα
def process_single_region_fixed_radius(weather_file, fire_file, region_center, fixed_radius_km):
    """
    Εφαρμογή του αλγορίθμου με σταθερή ακτίνα για την καθορισμένη περιοχή.
    """
    weather_data, fire_data = load_data(weather_file, fire_file)

    # Εφαρμογή αλγορίθμου με σταθερή ακτίνα για προσθήκη νέας στήλης
    enriched_weather_data = add_fire_column_fixed_radius(weather_data, fire_data, region_center, fixed_radius_km)

    return enriched_weather_data


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

# Υπολογισμός στατιστικών φωτιάς από το 2019 έως το 2023
total_fire_days, total_fires = fire_statistics(fire_data, 2019, 2023)

print("Συνολικές ημέρες φωτιάς:", total_fire_days)
print("Συνολικές φωτιές από το 2019 έως το 2023:", total_fires)

# Εκτέλεση της ανάλυσης για την περιοχή της Ανθούσας με σταθερή ακτίνα
enriched_data = process_single_region_fixed_radius(weather_file, fire_file, region_center, fixed_radius_km)

# Αποθήκευση του εμπλουτισμένου συνόλου δεδομένων στην επιφάνεια εργασίας
enriched_data.to_csv('/Users/giorgosziakas/Desktop/Anthousa_enriched_weather_data.csv', index=False)
