from random import uniform
from dotenv import load_dotenv
import os

load_dotenv('../keys.env')
api_key = os.getenv('API_KEY')
api_key_org = os.getenv('API_KEY_ORG')
import requests

def geocoder(address):
    geocoder_params = {"apikey": api_key,
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
        if json_response['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']:
            adress_index = json_response['metaDataProperty']['GeocoderMetaData']['Address']['postal_code']
            print(toponym_longitude, toponym_lattitude)
            return toponym_longitude, toponym_lattitude, full_result, adress_index
        elif json_response["Point"]["pos"].split(' '):
            return toponym_longitude, toponym_lattitude, full_result

    except Exception as e:
        print(f'Ошибка - {e}')
        return None



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

    try:
        if response := requests.get(url, params=params):
            with open("../picture.png", "wb") as file:
                file.write(response.content)
        return 'picture.png'
    except Exception as e:
        print(f"Ошибка выполнения запроса - {e}")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None



def get_adress(long, lat):
    geocoder_params = {"apikey": api_key,
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

    search_params = {
            "apikey": api_key_org,
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
