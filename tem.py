import requests
import json

# Make a GET request to the Flask route
response = requests.get(
    'http://localhost:5500/api/weather/HistoryDailyWeather/adilabad')

data = response.json()

# Iterate over the documents
for document in data:
    print(document)
