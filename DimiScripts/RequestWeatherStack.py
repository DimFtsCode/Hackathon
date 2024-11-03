import requests

api_key = "7bb6dcf6dccc3e10945b5033fffc3e9d"
latitude = 38.0733
longitude = 23.8701
url = f"http://api.weatherstack.com/current?access_key={api_key}&query={latitude},{longitude}"

response = requests.get(url)
data = response.json()

print(data)
