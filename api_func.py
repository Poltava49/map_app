from random import uniform
import requests

def geocoder(address):
    geocoder_params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
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


def get_image(toponym_longitude, toponym_lattitude, size):
    params = {
        'll': f"{toponym_longitude},{toponym_lattitude}",
        'spn': f'{size},{size}',
        'size': '650,450',
        'l': 'map',
        'z': 5
    }
    url = 'https://static-maps.yandex.ru/1.x/?'
    response = requests.get(url, params)

    if response := requests.get(url, params=params):
        with open("picture.png", "wb") as file:
            file.write(response.content)
        return 'picture.png'
    else:
        return None