from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from bson import ObjectId
from typing import List, Optional

# Router για τα endpoints
router = APIRouter()

# Μοντέλο δεδομένων
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

# Εξάρτηση για την MongoDB συλλογή
def get_weather_collection():
    from main import weather_collection  # Εισαγωγή από το main
    return weather_collection

# Endpoints

@router.post("/weather/", response_model=WeatherData)
def create_weather_data(weather: WeatherData, weather_collection=Depends(get_weather_collection)):
    weather_dict = weather.dict()
    weather_dict.pop("id", None)
    new_weather = weather_collection.insert_one(weather_dict)
    created_weather = weather_collection.find_one({"_id": new_weather.inserted_id})
    return weather_helper(created_weather)

@router.get("/weather/", response_model=List[WeatherData])
def get_all_weather_data(weather_collection=Depends(get_weather_collection)):
    weather_data = []
    for weather in weather_collection.find():
        weather_data.append(weather_helper(weather))
    return weather_data

@router.get("/weather/{weather_id}", response_model=WeatherData)
def get_weather_data(weather_id: str, weather_collection=Depends(get_weather_collection)):
    try:
        object_id = ObjectId(weather_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid ID format")
    
    weather = weather_collection.find_one({"_id": object_id})
    if weather:
        return weather_helper(weather)
    raise HTTPException(status_code=404, detail="Weather data not found")

@router.put("/weather/{weather_id}", response_model=WeatherData)
def update_weather_data(weather_id: str, weather: WeatherData, weather_collection=Depends(get_weather_collection)):
    try:
        object_id = ObjectId(weather_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid ID format")
    
    weather_dict = weather.dict()
    weather_dict.pop("id", None)
    updated_weather = weather_collection.find_one_and_update(
        {"_id": object_id}, {"$set": weather_dict}, return_document=True
    )
    if updated_weather:
        return weather_helper(updated_weather)
    raise HTTPException(status_code=404, detail="Weather data not found")

@router.delete("/weather/{weather_id}")
def delete_weather_data(weather_id: str, weather_collection=Depends(get_weather_collection)):
    try:
        object_id = ObjectId(weather_id)
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid ID format")
    
    delete_result = weather_collection.delete_one({"_id": object_id})
    if delete_result.deleted_count == 1:
        return {"message": "Weather data deleted successfully"}
    raise HTTPException(status_code=404, detail="Weather data not found")

@router.get("/weather/first", response_model=WeatherData)
def get_first_weather_data(weather_collection=Depends(get_weather_collection)):
    first_weather = weather_collection.find_one()
    if first_weather:
        return weather_helper(first_weather)
    raise HTTPException(status_code=404, detail="No weather data found")
