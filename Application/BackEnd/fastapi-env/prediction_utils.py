import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Ακτίνα της Γης σε χιλιόμετρα
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def calculate_bearing(lat1, lon1, lat2, lon2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)
    x = math.sin(delta_lambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - \
        math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    bearing = math.atan2(x, y)
    bearing = math.degrees(bearing)
    bearing = (bearing + 360) % 360  # Μετατροπή σε εύρος 0-360
    return bearing
def process_prediction_row(row, all_areas, critical_points_collection):
    prediction_value = row['prediction']
    message = ''
    at_risk_areas = []
    critical_points = []

    current_lat = row['latitude']
    current_lon = row['longitude']

    if prediction_value > 0.80:
        message = (
            "Υψηλός κίνδυνος πυρκαγιάς. "
            "Συνιστάται άμεση λήψη μέτρων πρόληψης, όπως η απομάκρυνση εύφλεκτων υλικών "
            "και η ενημέρωση των αρμόδιων αρχών για ενίσχυση της επιτήρησης."
        )
        wind_dir = row['wind_dir']  # σε μοίρες
        tolerance = 22.5  # Ανοχή για τον έλεγχο της κατεύθυνσης

        # Αναζήτηση περιοχών στην κατεύθυνση του ανέμου εντός 5 χλμ
        for idx, area in all_areas.iterrows():
            if area['name'] == row['name']:
                continue
            area_lat = area['latitude']
            area_lon = area['longitude']
            distance = haversine_distance(current_lat, current_lon, area_lat, area_lon)
            if distance <= 5.0:
                bearing = calculate_bearing(current_lat, current_lon, area_lat, area_lon)
                delta_angle = abs((bearing - wind_dir + 180) % 360 - 180)
                if delta_angle <= tolerance:
                    at_risk_areas.append({
                        'name': area['name'],
                        'distance_km': round(distance, 2),
                        'bearing': round(bearing, 2)
                    })

        # Αναζήτηση κρίσιμων σημείων εντός 5 χλμ
        critical_points_cursor = critical_points_collection.find({})
        for cp in critical_points_cursor:
            cp_lat = cp['latitude']
            cp_lon = cp['longitude']
            distance = haversine_distance(current_lat, current_lon, cp_lat, cp_lon)
            if distance <= 5.0:
                critical_points.append({
                    'description': cp['description'],
                    'area': cp['area'],
                    'distance_km': round(distance, 2)
                })

    elif 0.80 >= prediction_value >= 0.40:
        message = (
            "Μέτριος κίνδυνος πυρκαγιάς. "
            "Προτείνεται η ευαισθητοποίηση της κοινότητας για προληπτικά μέτρα "
            "και η ενίσχυση της επιτήρησης σε κρίσιμα σημεία."
        )

        # Αναζήτηση κρίσιμων σημείων εντός 5 χλμ
        critical_points_cursor = critical_points_collection.find({})
        for cp in critical_points_cursor:
            cp_lat = cp['latitude']
            cp_lon = cp['longitude']
            distance = haversine_distance(current_lat, current_lon, cp_lat, cp_lon)
            if distance <= 5.0:
                critical_points.append({
                    'description': cp['description'],
                    'area': cp['area'],
                    'distance_km': round(distance, 2)
                })

    else:
        message = (
            "Χαμηλός κίνδυνος πυρκαγιάς. "
            "Συνιστάται η διατήρηση των μέτρων πρόληψης και η τακτική επιτήρηση "
            "για την αποτροπή πιθανών κινδύνων."
        )

    # Προσθήκη των νέων πεδίων στο row
    row['message'] = message
    if at_risk_areas:
        row['at_risk_areas'] = at_risk_areas
    if critical_points:
        row['critical_points'] = critical_points

    return row

