from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import re
import math

# Initialize the OpenAI client 
client = OpenAI(api_key='Replace witho your OpenAI API key')

# MongoDB connection URI
mongo_uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
mongo_client = MongoClient(mongo_uri)

# Επιλογή βάσης δεδομένων και συλλογής
db = mongo_client["Weather"]
weather_collection = db["Hackathon"]
critical_infra_collection = db["CriticalInfra"]  # Collection for Critical Infrastructure

print("Connected to MongoDB successfully.")

# Φόρτωση του μοντέλου SentenceTransformer
embedding_model = SentenceTransformer("thenlper/gte-large")
print("Loaded SentenceTransformer model successfully.")

# Συνάρτηση για δημιουργία embedding
def get_embedding(text):
    if not text.strip():
        print("Attempted to get embedding for empty text.")
        return []

    embedding = embedding_model.encode(text)
    return embedding.tolist()

# Συνάρτηση για μετατροπή εγγραφής σε περιγραφικό κείμενο
def create_text_from_record(record):
    text = (f"Location: {record.get('name', 'Unknown')}, Latitude: {record.get('latitude', 'N/A')}, "
            f"Longitude: {record.get('longitude', 'N/A')}, Date: {record.get('date', 'N/A')}, "
            f"Time: {record.get('time', 'N/A')}, Temperature: {record.get('temperature', 'N/A')}°C, "
            f"Wind Speed: {record.get('wind_speed', 'N/A')} kph, Wind Direction: {record.get('wind_dir', 'N/A')}, "
            f"Humidity: {record.get('humidity', 'N/A')}%, Visibility: {record.get('visibility', 'N/A')} km")
    return text

# Συνάρτηση για εξαγωγή ημερομηνίας, τοποθεσίας και συντεταγμένων από το ερώτημα
def extract_date_location_coordinates(query):
    date_match = re.search(r"\d{4}-\d{2}-\d{2}", query)
    date = date_match.group(0) if date_match else None

    locations = ["Anthousa", "Dioni", "Melissia", "Marathon", "Nea Penteli"] # add all locations for final
    found_locations = []
    for loc in locations:
        if loc.lower() in query.lower():
            found_locations.append(loc)

    # Εξαγωγή συντεταγμένων
    lat_match = re.search(r"lat\s*[:=]\s*([0-9.\-]+)", query, re.IGNORECASE)
    lon_match = re.search(r"lon\s*[:=]\s*([0-9.\-]+)", query, re.IGNORECASE)
    latitude = float(lat_match.group(1)) if lat_match else None
    longitude = float(lon_match.group(1)) if lon_match else None

    return date, found_locations, latitude, longitude

# Συνάρτηση για αναζήτηση αποτελεσμάτων στη βάση δεδομένων
def query_results(query):
    query_embedding = get_embedding(query)
    date_filter, location_filters, _, _ = extract_date_location_coordinates(query)

    filter_conditions = {}
    if date_filter:
        filter_conditions['date'] = date_filter
    if location_filters:
        filter_conditions['name'] = {'$in': location_filters}

    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 150,
                "limit": 5
            }
        }
    ]

    if filter_conditions:
        pipeline[0]["$vectorSearch"]["filter"] = filter_conditions

    results = db.Hackathon.aggregate(pipeline)
    return list(results)

# Συνάρτηση για λήψη αποτελεσμάτων αναζήτησης και δημιουργία περιγραφής
def get_search_results(query):
    results = query_results(query)

    search_results = ""
    for result in results:
        search_results += create_text_from_record(result) + "\n"
    return search_results, results

# Συνάρτηση για λήψη κρίσιμων υποδομών με βάση τις συντεταγμένες
def get_critical_infra_descriptions(latitude, longitude, radius=0.01):
    if latitude is None or longitude is None:
        return []

    query = {
        "latitude": {"$gte": latitude - radius, "$lte": latitude + radius},
        "longitude": {"$gte": longitude - radius, "$lte": longitude + radius}
    }
    results = critical_infra_collection.find(query)
    descriptions = []
    for result in results:
        category = result.get("category", -1)
        if category is not None:
            category = int(category)
        else:
            category = -1

        descriptions.append({
            "description": result.get("description", "Unknown"),
            "category": category
        })
    return descriptions

# Συνάρτηση για μετατροπή κατεύθυνσης ανέμου σε μοίρες
def wind_direction_to_degrees(wind_dir):
    directions = {
        'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
        'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
        'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
        'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
    }
    return directions.get(wind_dir.upper(), None)

# Συνάρτηση για υπολογισμό κατεύθυνσης προς την οποία φυσάει ο άνεμος
def calculate_downwind_bearing(wind_deg):
    return (wind_deg + 180) % 360

# Συνάρτηση για υπολογισμό αρχικής πορείας μεταξύ δύο σημείων
def calculate_initial_compass_bearing(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    diff_lon = math.radians(lon2 - lon1)

    x = math.sin(diff_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - \
        (math.sin(lat1) * math.cos(lat2) * math.cos(diff_lon))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

# Συνάρτηση για υπολογισμό απόστασης μεταξύ δύο σημείων
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Ακτίνα της Γης σε χιλιόμετρα
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Συνάρτηση για έλεγχο αν ένα σημείο βρίσκεται εντός ενός τομέα
def is_within_sector(source_lat, source_lon, target_lat, target_lon, bearing, angle_range=45):
    initial_bearing = calculate_initial_compass_bearing(source_lat, source_lon, target_lat, target_lon)
    angle_diff = min((initial_bearing - bearing) % 360, (bearing - initial_bearing) % 360)
    return angle_diff <= (angle_range / 2)

# Συνάρτηση για παραγωγή της τελικής απάντησης χρησιμοποιώντας το OpenAI API
def generate_text(query):
    source_information, results = get_search_results(query)

    # Εξαγωγή συντεταγμένων από την ερώτηση
    _, _, query_latitude, query_longitude = extract_date_location_coordinates(query)

    # Λήψη κρίσιμων υποδομών με βάση τις συντεταγμένες
    critical_infra_descriptions = get_critical_infra_descriptions(query_latitude, query_longitude)

    if results:
        source_area = results[0]
        source_name = source_area.get('name')
        source_lat = source_area.get('latitude')
        source_lon = source_area.get('longitude')
        wind_dir = source_area.get('wind_dir')
        wind_deg = wind_direction_to_degrees(wind_dir)
        downwind_bearing = calculate_downwind_bearing(wind_deg)
    else:
        source_name = None
        source_lat = query_latitude
        source_lon = query_longitude
        wind_dir = None
        wind_deg = None
        downwind_bearing = None

    # Αν έχουμε συντεταγμένες και κατεύθυνση ανέμου
    at_risk_areas = []
    if source_lat and source_lon and downwind_bearing is not None:
        # Εύρεση άλλων περιοχών από τη συλλογή Hackathon
        radius_km = 20  # Ακτίνα σε χιλιόμετρα
        query = {
            "latitude": {"$exists": True},
            "longitude": {"$exists": True},
            "name": {"$ne": source_name}
        }
        other_areas = list(weather_collection.find(query))

        for area in other_areas:
            target_lat = area.get('latitude')
            target_lon = area.get('longitude')
            if target_lat and target_lon:
                distance = haversine_distance(source_lat, source_lon, target_lat, target_lon)
                if distance <= radius_km:
                    if is_within_sector(source_lat, source_lon, target_lat, target_lon, downwind_bearing):
                        at_risk_areas.append(area.get('name'))

    # Αφαίρεση διπλότυπων
    at_risk_areas = list(set(at_risk_areas))

    # Δημιουργία περιεχομένου για το LLM
    combined_information = f"Question: {query}\n"

    if source_information.strip():
        combined_information += (
            f"Using the following weather information, answer the question:\n"
            f"{source_information}\n"
        )
    else:
        combined_information += "I couldn't find specific weather data matching your query.\n"

    if critical_infra_descriptions:
        combined_information += "Important nearby locations based on provided coordinates:\n"
        for desc in critical_infra_descriptions:
            category = desc['category']
            description = desc['description']
            if category == 0:
                importance = f"{description} (Drone location)"
            elif category == 1:
                importance = f"{description} (Fire Station - can assist quickly in emergencies)"
            elif category == 2:
                importance = f"{description} (Police Station - important for security)"
            elif category == 3:
                importance = f"{description} (Critical facility such as hospital or educational institution)"
            else:
                importance = description  # For unknown category
            combined_information += f"- {importance}\n"
    else:
        combined_information += "No critical infrastructure found near the provided coordinates.\n"

    # Προσθήκη περιοχών που κινδυνεύουν
    if at_risk_areas:
        combined_information += "\nBased on the wind direction and speed, the following nearby areas may be at risk:\n"
        for area in at_risk_areas:
            combined_information += f"- {area}\n"
    else:
        combined_information += "\nNo nearby areas are identified as at risk based on the wind direction and proximity.\n"

    # Ζητήστε από το LLM να παρέχει σχόλια
    combined_information += "\nPlease provide a brief commentary on the weather conditions,alert for sending drones for surveillance and emergency response, the importance of the nearby locations, and the potential risks to the areas listed above.\n"

    # Κλήση του OpenAI API
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that provides precise weather information "
                    "Alerts for sending drones for surveillance and emergency response. "
                    "and highlights important nearby locations based on the user's query. "
                    "Using the wind direction from the provided weather data, identify nearby areas that might be at risk "
                    "due to the wind conditions, based on your knowledge of the geography. "
                    "Present the information in clear, well-organized markdown tables and provide a brief commentary on the results."
                )
            },
            {"role": "user", "content": combined_information}
        ],
        max_tokens=500,
        temperature=0.7
    )

    answer = response.choices[0].message.content.strip()
    return answer

# Παράδειγμα χρήσης
if __name__ == "__main__":
    query = "What are the weather conditions in Anthousa on 2019-05-01? Also, what important locations are near lat:38.0576 lon:23.8433?"
    answer = generate_text(query)
    print("Answer:")
    print(answer)



    









