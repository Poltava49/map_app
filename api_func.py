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
    toponym_longitude, toponym_lattitude = json_response["Point"]["pos"].split(' ')
    try:
        adress_index = json_response['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']

        return toponym_longitude, toponym_lattitude, full_result, adress_index
    except:
        print('Ошибка')
        return toponym_longitude, toponym_lattitude, full_result


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
    print(response.url)

    if response := requests.get(url, params=params):
        with open("picture.png", "wb") as file:
            file.write(response.content)
        return 'picture.png'
    else:
        print("Ошибка выполнения запроса")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None



def get_adress(long, lat):
    geocoder_params = {"apikey": "8287b6ed-122d-48e1-a4f0-1e1f09386c0f",
                       "geocode": f'{long},{lat}',
                       "format": "json",
                       "lang": "ru_RU"
                       }
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None
    json_response = (response.json())["response"]["GeoObjectCollection"]['featureMember'][0]["GeoObject"]
    print(response.json())
    full_adress = json_response['metaDataProperty']['GeocoderMetaData']['text']
    try:
        adress_index = json_response['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
        return full_adress, adress_index
    except KeyError:
        print('Ошибка запроса')
        return full_adress




def get_organization(adress, long, lat):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key ="dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
            "apikey": api_key,
            "lang": "ru_RU",
            "text": adress,
            "ll": f"{long},{lat}",
            "type": "biz",
            "spn": f"{0.01},{0.01}"

        }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None
    try:
        org_name = response.json()['features'][1]['properties']['name']
        org_type = response.json()['features'][1]['properties']['CompanyMetaData']['Categories'][0]['name']
        return f'{org_type} - {org_name}'
    except:
        return 'Организаций нет'
