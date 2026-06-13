import requests

API_KEY = "3a5673d4aa8e6c5a869aa684f6b44d03"

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    return response.json()