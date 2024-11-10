import pandas as pd
from pymongo import MongoClient
import os 

# Path to the csv file
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "Dioni_weather_data.csv")


# Read the csv file into a pandas DataFrame
try:
    
    df = pd.read_csv(desktop_path)
    print("File read successfully.")
except FileNotFoundError:
    print("File not found. Please check the path.")
    exit()
    
# Replace with your actual MongoDB URI
uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
client = MongoClient(uri)

# Access the 'Weather' database and 'Hackathon' collection
db = client['Weather']
collection = db['Hackathon']

# Convert DataFrame rows to dictionaries
data = df.to_dict(orient='records')

# Insert the data into MongoDB
if data:
    collection.insert_many(data)
    print("Data uploaded successfully to the Hackathon collection in MongoDB!")
    
    # Verify upload by counting documents
    count = collection.count_documents({})
    print(f"Total documents in 'Hackathon' collection after upload: {count}")
else:
    print("No data found in the CSV file.")
    
    
# Retrieve and print the last 5 documents
print("Last 5 documents from 'Hackathon' collection:")
for doc in collection.find().sort('_id', -1).limit(5):
    print(doc)
    
# Ελέγχουμε τη σύνδεση με τη MongoDB και ανακτούμε τα δεδομένα από τη συλλογή "Hackathon"
db = client["Weather"]  # Πρόσβαση στη βάση δεδομένων Weather
hackathon_collection = db["Hackathon"]  # Πρόσβαση στη συλλογή Hackathon

# Ανάκτηση όλων των δεδομένων από τη συλλογή
data = hackathon_collection.find()

# Εκτύπωση των δεδομένων
for document in data:
    print(document)
    
# Προσδιορισμός των βασικών πεδίων των δεδομένων καιρού
# Ορισμός βασικών πεδίων που πρέπει να υπάρχουν στα έγγραφα καιρού
weather_fields = ["name", "latitude", "longitude", "date", "time", "temperature", "wind_speed", "wind_dir", "humidity", "visibility"]

# Διαγραφή εγγράφων που δεν περιέχουν όλα τα βασικά πεδία δεδομένων καιρού
hackathon_collection.delete_many({
    "$or": [{field: {"$exists": False}} for field in weather_fields]
})

print("Non-weather data documents have been removed from the collection.")