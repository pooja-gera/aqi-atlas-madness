import json
from bson import json_util
import os
from flask import request, jsonify, make_response
from app import app
from .utils import prepare_data_for_api, prepare_history_data
from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv('.env')

client = MongoClient(
    "mongodb+srv://pooja-gera:SdQm6tFSf333SuZO@cluster1.1mza7mx.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('aqi')
# print(db)

app = Flask(__name__)


def remove_objectid(doc):
    doc.pop('_id', None)
    return doc


@app.route("/", methods=['GET'])
def index():
    data = {"text": "Hello World"}
    return (jsonify(data))


@app.route("/api/aqi/MonthlyAQIPredictions/<city>", methods=['GET'])
def MonthlyAQIPredictions(city):
    city = city
    collection = db['aqi_forecast_monthly_collection']
    data = collection.find({'city': city})

    # Remove the ObjectId field from each document
    documents = [remove_objectid(doc) for doc in data]

    # Create a JSON object with the city as the main key
    result = {city: documents}

    # Convert result to JSON
    json_result = json.dumps(result)

    return json_result


@ app.route("/api/aqi/DailyAQIPredictions/<city>", methods=['GET'])
def DailyAQIPredictions(city):
    city = city
    collection = db['aqi_forecast_daily_collection']
    data = collection.find({'city': city})

    # Remove the ObjectId field from each document
    documents = [remove_objectid(doc) for doc in data]

    # Create a JSON object with the city as the main key
    result = {city: documents}

    # Convert result to JSON
    json_result = json.dumps(result)

    return json_result


@ app.route("/api/weather/MonthlyWeatherPredictions/<city>", methods=['GET'])
def MonthlyWeatherPredictions(city):
    city = city
    collection = db['weather_forecast_monthly_collection']
    data = collection.find({'city': city})

    # Remove the ObjectId field from each document
    documents = [remove_objectid(doc) for doc in data]

    # Create a JSON object with the city as the main key
    result = {city: documents}

    # Convert result to JSON
    json_result = json.dumps(result)

    return json_result


@ app.route("/api/weather/DailyWeatherPredictions/<city>", methods=['GET'])
def DailyWeatherPredictions(city):
    city = city
    collection = db['weather_forecast_daily_collection']
    data = collection.find({'city': city})
    for d in data:
        print(d)
    # Remove the ObjectId field from each document
    documents = [remove_objectid(doc) for doc in data]

    # Create a JSON object with the city as the main key
    result = {city: documents}

    # Convert result to JSON
    json_result = json.dumps(result)

    return json_result


@ app.route("/api/aqi/HistoryMonthlyAQI/<city>", methods=['GET'])
def HistoryMonthlyAQI(city):
    city = city
    collection = db['AQI_history_monthly_collection']
    data = collection.find({'city': city})

    # Remove the ObjectId field from each document
    documents = [remove_objectid(doc) for doc in data]

    # Create a JSON object with the city as the main key
    result = {city: documents}

    # Convert result to JSON
    json_result = json.dumps(result)

    return json_result


@ app.route("/api/aqi/HistoryDailyAQI/<city>", methods=['GET'])
def HistoryDailyAQI(city):
    city = city
    collection = db['AQI_history_daily_collection']
    data = collection.find({'city': city})

    # Remove the ObjectId field from each document
    documents = [remove_objectid(doc) for doc in data]

    # Create a JSON object with the city as the main key
    result = {city: documents}

    # Convert result to JSON
    json_result = json.dumps(result)

    return json_result


@ app.route("/api/weather/HistoryMonthlyWeather/<city>", methods=['GET'])
def HistoryMonthlyWeather(city):
    city = city
    collection = db['weather_history_monthly_collection']
    print(city, "===")
    data = collection.find({'city': city})

    # Remove the ObjectId field from each document
    documents = [remove_objectid(doc) for doc in data]

    # Create a JSON object with the city as the main key
    result = {city: documents}

    # Convert result to JSON
    json_result = json.dumps(result)

    return json_result


@ app.route("/api/weather/HistoryDailyWeather/<city>", methods=['GET'])
def HistoryDailyWeather(city):
    city = city
    print(city, "===")
    collection = db['weather_history_dailly_collection']
    data = collection.find({'city': city})

    # Remove the ObjectId field from each document
    documents = [remove_objectid(doc) for doc in data]

    # Create a JSON object with the city as the main key
    result = {city: documents}

    # Convert result to JSON
    json_result = json.dumps(result)

    return json_result

# @ app.route("/api/aqi/getMonthlyAQIPredictions", methods=['POST'])
# def getMonthlyAQIPredictions():
#     city = request.json.get('City')
#     forecast_type = 'monthly'
#     parameter_type = 'aqi'
#     return make_response(prepare_data_for_api(city, forecast_type, parameter_type))


# @ app.route("/api/aqi/getDailyAQIPredictions", methods=['POST'])
# def getDailyAQIPredictions():
#     city = request.json.get('City')
#     forecast_type = 'daily'
#     parameter_type = 'aqi'
#     return make_response(prepare_data_for_api(city, forecast_type, parameter_type))


# @ app.route("/api/weather/getMonthlyWeatherPredictions", methods=['POST'])
# def getMonthlyWeatherPredictions():
#     city = request.json.get('City')
#     forecast_type = 'monthly'
#     parameter_type = 'weather'
#     return make_response(prepare_data_for_api(city, forecast_type, parameter_type))


# @ app.route("/api/weather/getDailyWeatherPredictions", methods=['POST'])
# def getDailyWeatherPredictions():
#     city = request.json.get('City')
#     forecast_type = 'daily'
#     parameter_type = 'weather'
#     return make_response(prepare_data_for_api(city, forecast_type, parameter_type))


# @ app.route("/api/aqi/getHistoryMonthlyAQI", methods=['POST'])
# def getHistoryMonthlyAQI():
#     city = request.json.get('City')
#     forecast_type = 'monthly'
#     parameter_type = 'aqi'
#     return make_response(prepare_history_data(city, forecast_type, parameter_type))


# @ app.route("/api/aqi/getHistoryDailyAQI", methods=['POST'])
# def getHistoryDailyAQI():
#     city = request.json.get('City')
#     forecast_type = 'daily'
#     parameter_type = 'aqi'
#     return make_response(prepare_history_data(city, forecast_type, parameter_type))


# @ app.route("/api/weather/getHistoryMonthlyWeather", methods=['POST'])
# def getHistoryMonthlyWeather():
#     city = request.json.get('City')
#     forecast_type = 'monthly'
#     parameter_type = 'weather'
#     return make_response(prepare_history_data(city, forecast_type, parameter_type))


# @ app.route("/api/weather/getHistoryDailyWeather", methods=['POST'])
# def getHistoryDailyWeather():
#     city = request.json.get('City')
#     forecast_type = 'daily'
#     parameter_type = 'weather'
#     return make_response(prepare_history_data(city, forecast_type, parameter_type))
