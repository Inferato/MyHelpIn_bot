import requests


def getweather(city):
    url = "https://community-open-weather-map.p.rapidapi.com/weather"
    querystring = {"q": city + ",ua", "lang": "ru", "units": "metric", "mode": "JSON"}
    headers = {
        'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
        'x-rapidapi-key': "4181fff725mshd7364bf0e3a7f1bp1e193djsn4837a2d14901"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    return response
