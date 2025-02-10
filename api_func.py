from random import uniform
import requests

def geocoder(address):
    geocoder_params = {"apikey": "8287b6ed-122d-48e1-a4f0-1e1f09386c0f",
                       "geocode": address,
                       "format": "json",
                       "kind": "district"
                       }
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    toponym_longitude, toponym_lattitude = \
    json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(' ')
    return toponym_longitude, toponym_lattitude


def get_image(toponym_longitude, toponym_lattitude, size, map_type):
    params = {
        'll': f"{toponym_longitude},{toponym_lattitude}",
        'spn': f'{size},{size}',
        'size': '650,450',
        'l': map_type,
        'z': 2
    }
    url = 'https://static-maps.yandex.ru/1.x/?'
    response = requests.get(url, params)


    if response := requests.get(url, params=params):
        with open("picture.png", "wb") as file:
            file.write(response.content)
        return 'picture.png'
    else:
        return None