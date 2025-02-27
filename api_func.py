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
        print("Ошибка выполнения запроса: Tut ")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None
    json_response = (response.json())["response"]["GeoObjectCollection"]['featureMember'][0]["GeoObject"]
    full_result = json_response['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
    adress_index = json_response['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    toponym_longitude, toponym_lattitude = json_response["Point"]["pos"].split(' ')
    return toponym_longitude, toponym_lattitude, full_result, adress_index


def get_image(toponym_longitude, toponym_lattitude, size, map_type, point):
    params = {
        'll': f"{toponym_longitude},{toponym_lattitude}",
        'spn': f'{size},{size}',
        'size': '650,450',
        'l': map_type,
        'z': 2,
        'pt': point
    }
    url = 'https://static-maps.yandex.ru/1.x/?'
    response = requests.get(url, params)

    if response := requests.get(url, params=params):
        with open("picture.png", "wb") as file:
            file.write(response.content)
        return 'picture.png'
    else:
        print("Ошибка выполнения запроса: Tut ")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None


# def geocoder_point(long, lat):
#     geocoder_params = {"apikey": "8287b6ed-122d-48e1-a4f0-1e1f09386c0f",
#                        "geocode": f'{long, lat}',
#                        "format": "json"
#                        }
#     geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
#     response = requests.get(geocoder_api_server, params=geocoder_params)
#

def get_adress(long, lat):
    geocoder_params = {"apikey": "8287b6ed-122d-48e1-a4f0-1e1f09386c0f",
                       "geocode": f'{long},{lat}',
                       "format": "json",
                       "lang": "ru_RU"
                       }
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print("Ошибка выполнения запроса: Tut ")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None
    json_response = (response.json())["response"]["GeoObjectCollection"]['featureMember'][0]["GeoObject"]
    full_adress = json_response['metaDataProperty']['GeocoderMetaData']['text']
    adress_index = json_response['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
    return full_adress, adress_index