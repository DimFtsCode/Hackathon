def get_weather_data_by_coordinates(api_key, latitude, longitude):
    base_url = "http://api.weatherstack.com/current"

    params = {
        'access_key': api_key,
        'query': f"{latitude},{longitude}",
        'units': 'm'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'current' in data:
            current_weather = data['current']
            print(f"Καιρός για συντεταγμένες: {latitude}, {longitude}")
            print(f"Θερμοκρασία: {current_weather['temperature']}°C")
            print(f"Αίσθηση: {current_weather['feelslike']}°C")
            print(f"Υγρασία: {current_weather['humidity']}%")
            print(f"Ταχύτητα ανέμου: {current_weather['wind_speed']} km/h")
            print(f"Κατεύθυνση ανέμου: {current_weather['wind_dir']}")
            print(f"Συνθήκες: {current_weather['weather_descriptions'][0]}")
        else:
            print("Δεν βρέθηκαν δεδομένα για τις συντεταγμένες που δόθηκαν.")
    else:
        print(f"Σφάλμα: Δεν ήταν δυνατή η λήψη των δεδομένων. Κωδικός κατάστασης: {response.status_code}")

# Παράδειγμα κλήσης με συντεταγμένες για την Πεντέλη
api_key = 'YOUR_API_KEY'
get_weather_data_by_coordinates(api_key, 38.05, 23.87)
