import math

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # Earth's radius in kilometers
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
    bearing = (bearing + 360) % 360  # Convert to range 0-360
    return bearing

def process_prediction_row(row, all_areas, critical_points_collection):
    prediction_value = row['prediction']
    message = ''
    current_lat = row['latitude']
    current_lon = row['longitude']

    # Nearest drone, fire station, and police station
    nearest_drone = None
    nearest_fire_station = None
    nearest_police_station = None
    min_drone_distance = float('inf')
    min_fire_station_distance = float('inf')
    min_police_station_distance = float('inf')

    # Find critical points
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
            "High wildfire risk. "
            "Immediate preventive measures are recommended, such as removing flammable materials "
            "and notifying the relevant authorities to enhance surveillance.\n"
        )

        # Drone activation
        if nearest_drone:
            travel_time = min_drone_distance / 50.0  # Assuming drone speed 50 km/h
            bearing = calculate_bearing(
                nearest_drone['latitude'], nearest_drone['longitude'],
                current_lat, current_lon
            )
            message += (
                f" Drone activation from the area '{nearest_drone['description']}'. "
                f"Arrival time: {round(travel_time * 60, 2)} minutes. "
                f"Direction: {round(bearing, 2)} degrees.\n"
            )

        # Fire Station response
        if nearest_fire_station:
            message += (
                f"1) Fire Station at '{nearest_fire_station['description']}' "
                f"should immediately monitor the area.\n"
            )

        # Police Station response
        if nearest_police_station:
            message += (
                f"2) Police Station at '{nearest_police_station['description']}' "
                f"should immediately secure the area.\n"
            )

        # Critical points (category = 3) within 5 km
        critical_points_cursor = critical_points_collection.find({'category': 3})
        for cp in critical_points_cursor:
            cp_lat = cp['latitude']
            cp_lon = cp['longitude']
            distance = haversine_distance(current_lat, current_lon, cp_lat, cp_lon)

            if distance <= 5.0 and nearest_drone:
                travel_time = distance / 50.0  # Assuming drone speed 50 km/h
                bearing = calculate_bearing(
                    nearest_drone['latitude'], nearest_drone['longitude'],
                    cp_lat, cp_lon
                )
                message += (
                    f"3) Protect critical points, such as the school/hospital in the area "
                    f"'{cp['description']}'. Activate drone from the area "
                    f"'{nearest_drone['description']}' for surveillance. "
                    f"Arrival time: {round(travel_time * 60, 2)} minutes. "
                    f"Direction: {round(bearing, 2)} degrees.\n"
                )

    elif 0.80 >= prediction_value >= 0.40:
        message = (
            "Moderate wildfire risk. "
            "Community awareness for preventive measures is recommended, along with enhanced surveillance.\n"
        )

        # Drone activation
        if nearest_drone:
            travel_time = min_drone_distance / 50.0  # Assuming drone speed 50 km/h
            bearing = calculate_bearing(
                nearest_drone['latitude'], nearest_drone['longitude'],
                current_lat, current_lon
            )
            message += (
                f" Drone activation from the area '{nearest_drone['description']}'. "
                f"Arrival time: {round(travel_time * 60, 2)} minutes. "
                f"Direction: {round(bearing, 2)} degrees.\n"
            )

    else:
        message = (
            "Low wildfire risk.\n"
        )

    # Return the message
    row['message'] = message
    return row
