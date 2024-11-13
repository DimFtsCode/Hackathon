from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from typing import List, Optional

# Αρχικοποίηση του FastAPI app
app = FastAPI()

# Σύνδεση με τη MongoDB
mongo_uri = "mongodb+srv://GiorgosZiakas:AdGiorgosMin24@cluster0.itaqk.mongodb.net/Weather"
mongo_client = MongoClient(mongo_uri)
db = mongo_client["Weather"]
weather_collection = db["Hackathon"]

print("Connected to MongoDB successfully.")

# Μοντέλο δεδομένων για εισαγωγή και ανάκτηση πληροφοριών
class WeatherData(BaseModel):
    location: str
    temperature: float
    humidity: float
    description: Optional[str] = None

# Βοηθητική συνάρτηση για μετατροπή δεδομένων MongoDB σε JSON format
def weather_helper(weather) -> dict:
    return {
        "id": str(weather["_id"]),
        "location": weather["location"],
        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "description": weather.get("description"),
    }

# Endpoint για δημιουργία νέας εγγραφής και εισαγωγή της στη βάση
@app.post("/weather/", response_model=WeatherData)
def create_weather_data(weather: WeatherData):
    weather_dict = weather.dict()
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
    updated_weather = weather_collection.find_one_and_update(
        {"_id": ObjectId(weather_id)}, {"$set": weather.dict()}, return_document=True
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
