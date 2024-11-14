from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Αρχικοποίηση του FastAPI app
app = FastAPI()

# Σύνδεση με τη MongoDB
mongo_uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
mongo_client = MongoClient(mongo_uri)
db = mongo_client["Weather"]
weather_collection = db["Hackathon"]

print("Connected to MongoDB successfully.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Επιτρέπει αιτήσεις μόνο από το React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Μοντέλο δεδομένων για εισαγωγή και ανάκτηση πληροφοριών
class WeatherData(BaseModel):
    id: Optional[str]
    name: str
    latitude: float
    longitude: float
    date: str
    time: int
    temperature: int
    wind_speed: int
    wind_dir: str
    humidity: int
    visibility: int

# Βοηθητική συνάρτηση για μετατροπή δεδομένων MongoDB σε JSON format
def weather_helper(weather) -> dict:
    return {
        "id": str(weather["_id"]),
        "name": weather.get("name", "Unknown"),
        "latitude": float(weather.get("latitude", 0)),
        "longitude": float(weather.get("longitude", 0)),
        "date": weather.get("date", "Unknown"),
        "time": int(weather.get("time", 0)),
        "temperature": int(weather.get("temperature", 0)),
        "wind_speed": int(weather.get("wind_speed", 0)),
        "wind_dir": weather.get("wind_dir", "Unknown"),
        "humidity": int(weather.get("humidity", 0)),
        "visibility": int(weather.get("visibility", 0))
    }

# Endpoint για δημιουργία νέας εγγραφής και εισαγωγή της στη βάση
@app.post("/weather/", response_model=WeatherData)
def create_weather_data(weather: WeatherData):
    weather_dict = weather.dict()
    weather_dict.pop("id", None)  # Remove 'id' if it exists, as MongoDB will auto-generate it
    new_weather = weather_collection.insert_one(weather_dict)
    created_weather = weather_collection.find_one({"_id": new_weather.inserted_id})
    return weather_helper(created_weather)

# Endpoint για ανάκτηση όλων των δεδομένων
@app.get("/weather/", response_model=List[WeatherData])
def get_all_weather_data():
    weather_data = []
    for weather in weather_collection.find():
        weather_data.append(weather_helper(weather))
    return weather_data

# Endpoint για ανάκτηση συγκεκριμένης εγγραφής βάσει ID
@app.get("/weather/{weather_id}", response_model=WeatherData)
def get_weather_data(weather_id: str):
    weather = weather_collection.find_one({"_id": ObjectId(weather_id)})
    if weather:
        return weather_helper(weather)
    raise HTTPException(status_code=404, detail="Weather data not found")

# Endpoint για ενημέρωση εγγραφής βάσει ID
@app.put("/weather/{weather_id}", response_model=WeatherData)
def update_weather_data(weather_id: str, weather: WeatherData):
    weather_dict = weather.dict()
    weather_dict.pop("id", None)  # Remove 'id' if it exists
    updated_weather = weather_collection.find_one_and_update(
        {"_id": ObjectId(weather_id)}, {"$set": weather_dict}, return_document=True
    )
    if updated_weather:
        return weather_helper(updated_weather)
    raise HTTPException(status_code=404, detail="Weather data not found")

# Endpoint για διαγραφή εγγραφής βάσει ID
@app.delete("/weather/{weather_id}")
def delete_weather_data(weather_id: str):
    delete_result = weather_collection.delete_one({"_id": ObjectId(weather_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Weather data deleted successfully"}
    raise HTTPException(status_code=404, detail="Weather data not found")

# Endpoint για εμφάνιση της πρώτης εγγραφής στο dataset
@app.get("/weather/first", response_model=WeatherData)
def get_first_weather_data():
    first_weather = weather_collection.find_one()  # Query χωρίς φίλτρο για να πάρουμε την πρώτη εγγραφή
    if first_weather:
        return weather_helper(first_weather)
    raise HTTPException(status_code=404, detail="No weather data found")
