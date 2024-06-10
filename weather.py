import requests
from num2words import num2words
import json
import datetime
import os

def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        'lang': "ru",
        "units": "metric"
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            temperature_text = num2words(int(temperature), lang='ru')
            return weather_description, temperature_text, data
        else:
            return None, None, None
    except requests.exceptions.RequestException:
        return None, None, None

def get_weather_tomorrow(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": api_key,
        'lang': "ru",
        "units": "metric",
        "cnt": 16
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            tomorrow_data = data['list'][8]
            weather_description = tomorrow_data['weather'][0]['description']
            temperature = tomorrow_data['main']['temp']
            temperature_text = num2words(int(temperature), lang='ru')
            return weather_description, temperature_text, tomorrow_data
        else:
            return None, None, None
    except requests.exceptions.RequestException as e:
        return None, None, None

def save_weather_to_json(data, tomorrow_data):
    weather_data = {
        "today": data,
        "tomorrow": tomorrow_data
    }
    with open("weather_data.json", "w", encoding='utf-8') as file:
        json.dump(weather_data, file, ensure_ascii=False, indent=4)

def load_weather_from_json():
    if os.path.exists("weather_data.json"):
        with open("weather_data.json", "r", encoding='utf-8') as file:
            data = json.load(file)
            return data
    return None

def check_internet_connection():
    try:
        requests.get("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def update_weather(api_key, city):
    internet_available = check_internet_connection()
    if internet_available:
        weather_description, temperature_text, data = get_weather(api_key, city)
        weather_description_tomorrow, temperature_text_tomorrow, tomorrow_data = get_weather_tomorrow(api_key, city)
        if weather_description is not None and weather_description_tomorrow is not None:
            save_weather_to_json(data, tomorrow_data)
        else:
            print("Помилка отримання даних про погоду.")
    else:
        print("Немає підключення до інтернету, але я можу подивитися, який прогноз завантажувався раніше!")