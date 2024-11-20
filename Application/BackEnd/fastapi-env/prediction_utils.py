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
    current_lat = row['latitude']
    current_lon = row['longitude']

    # Κοντινότερο drone, fire station και police station
    nearest_drone = None
    nearest_fire_station = None
    nearest_police_station = None
    min_drone_distance = float('inf')
    min_fire_station_distance = float('inf')
    min_police_station_distance = float('inf')

    # Εύρεση κρίσιμων σημείων
    critical_points_cursor = critical_points_collection.find({})
    for cp in critical_points_cursor:
        cp_lat = cp['latitude']
        cp_lon = cp['longitude']
        distance = haversine_distance(current_lat, current_lon, cp_lat, cp_lon)

        if cp['category'] == 0 and distance < min_drone_distance:  # Drone
            nearest_drone = cp
            min_drone_distance = distance
        elif cp['category'] == 1 and distance < min_fire_station_distance:  # Fire Station
            nearest_fire_station = cp
            min_fire_station_distance = distance
        elif cp['category'] == 2 and distance < min_police_station_distance:  # Police Station
            nearest_police_station = cp
            min_police_station_distance = distance

    if prediction_value > 0.80:
        message = (
            "Υψηλός κίνδυνος πυρκαγιάς. "
            "Συνιστάται άμεση λήψη μέτρων πρόληψης, όπως η απομάκρυνση εύφλεκτων υλικών "
            "και η ενημέρωση των αρμόδιων αρχών για ενίσχυση της επιτήρησης.\n"
        )

        # Drone ενεργοποίηση
        if nearest_drone:
            travel_time = min_drone_distance / 50.0  # Υποθέτουμε ταχύτητα drone 50 km/h
            bearing = calculate_bearing(
                nearest_drone['latitude'], nearest_drone['longitude'],
                current_lat, current_lon
            )
            message += (
                f" Ενεργοποίηση drone από την περιοχή '{nearest_drone['description']}'. "
                f"Χρόνος άφιξης: {round(travel_time * 60, 2)} λεπτά. "
                f"Κατεύθυνση: {round(bearing, 2)} μοίρες.\n"
            )

        # Fire Station επιτήρηση
        if nearest_fire_station:
            message += (
                f"1) Το Πυροσβεστικό Σώμα από τον σταθμό '{nearest_fire_station['description']}' "
                f"να επιτηρήσει άμεσα την περιοχή.\n"
            )

        # Police Station επιτήρηση
        if nearest_police_station:
            message += (
                f"2) Το Αστυνομικό Τμήμα από την περιοχή '{nearest_police_station['description']}' "
                f"να προστατεύσει άμεσα την περιοχή.\n"
            )

        # Εξετάζουμε κρίσιμα σημεία (category = 3) εντός 5 χλμ
        critical_points_cursor = critical_points_collection.find({'category': 3})
        for cp in critical_points_cursor:
            cp_lat = cp['latitude']
            cp_lon = cp['longitude']
            distance = haversine_distance(current_lat, current_lon, cp_lat, cp_lon)

            if distance <= 5.0 and nearest_drone:
                travel_time = distance / 50.0  # Υποθέτουμε ταχύτητα drone 50 km/h
                bearing = calculate_bearing(
                    nearest_drone['latitude'], nearest_drone['longitude'],
                    cp_lat, cp_lon
                )
                message += (
                    f"3)Προστασία κρίσιμων σημείων, όπως το σχολείο/νοσοκομείο στην περιοχή "
                    f"'{cp['description']}'. Ενεργοποίηση drone από την περιοχή "
                    f"'{nearest_drone['description']}' για επιτήρηση. "
                    f"Χρόνος άφιξης: {round(travel_time * 60, 2)} λεπτά. "
                    f"Κατεύθυνση: {round(bearing, 2)} μοίρες.\n"
                )

    elif 0.80 >= prediction_value >= 0.40:
        message = (
            "Μέτριος κίνδυνος πυρκαγιάς. "
            "Συνιστάται ευαισθητοποίηση της κοινότητας για προληπτικά μέτρα και "
            "ενίσχυση της επιτήρησης.\n"
        )

        # Drone ενεργοποίηση
        if nearest_drone:
            travel_time = min_drone_distance / 50.0  # Υποθέτουμε ταχύτητα drone 50 km/h
            bearing = calculate_bearing(
                nearest_drone['latitude'], nearest_drone['longitude'],
                current_lat, current_lon
            )
            message += (
                f" Ενεργοποίηση drone από την περιοχή '{nearest_drone['description']}'. "
                f"Χρόνος άφιξης: {round(travel_time * 60, 2)} λεπτά. "
                f"Κατεύθυνση: {round(bearing, 2)} μοίρες.\n"
            )

    else:
        message = (
            "Χαμηλός κίνδυνος πυρκαγιάς. \n"
        )

    # Επιστροφή του μηνύματος
    row['message'] = message
    return row