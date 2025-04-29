import logging
from src.config import CACHE_PATH, CACHED_IMAGE_NAME
from src.cache import read_from_cache, write_to_cache, check_cached
from random import uniform
from dotenv import load_dotenv
import os

load_dotenv("../keys.env")
api_key = os.getenv("API_KEY")
api_key_org = os.getenv("API_KEY_ORG")
print(api_key)
import requests


def geocoder(address) -> tuple | None:
    geocoder_params = {
        "apikey": api_key,
        "geocode": address,
        "format": "json",
        "kind": "district",
    }
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_api_server, params=geocoder_params)
    print(response.content)

    if not response:
        print("Ошибка выполнения запроса: Tut ")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None
    json_response = (response.json())["response"]["GeoObjectCollection"][
        "featureMember"
    ][0]["GeoObject"]
    full_result = json_response["metaDataProperty"]["GeocoderMetaData"]["Address"][
        "formatted"
    ]
    toponym_longitude, toponym_lattitude = json_response["Point"]["pos"].split(" ")
    try:
        if json_response["metaDataProperty"]["GeocoderMetaData"]["Address"][
            "postal_code"
        ]:
            adress_index = json_response["metaDataProperty"]["GeocoderMetaData"][
                "Address"
            ]["postal_code"]
            print(toponym_longitude, toponym_lattitude)
            return toponym_longitude, toponym_lattitude, full_result, adress_index
        elif json_response["Point"]["pos"].split(" "):
            return toponym_longitude, toponym_lattitude, full_result

    except Exception as e:
        print(f"Ошибка - {e}")
        return None


def get_image(
    toponym_longitude, toponym_lattitude, size, map_type, point
) -> bytes | None:
    params = {
        "apikey": api_key,
        "ll": f"{toponym_longitude},{toponym_lattitude}",
        "spn": f"{size},{size}",
        "size": "650,450",
        "l": map_type,
        "z": 2,
        "pt": point,
    }
    url = "https://static-maps.yandex.ru/1.x/?"
    response = requests.get(url, params)

    if check_cached(url, params):
        return read_from_cache(url, params)

    try:
        if response := requests.get(url, params=params):
            write_to_cache(
                request_url=url,
                request_params=params,
                resposne_status_code=response.status_code,
                is_file=True,
                content=response.content,
            )
            return response.content
        else:
            logging.warning(f"Не удалось получить картинку: url={url}")
            return None
    except Exception as e:
        logging.error(f"Ошибка выполнения запроса - {e}")
        logging.info("Http статус: ", response.status_code, "(", response.reason, ")")
        return None


def get_adress(long, lat):
    geocoder_params = {
        "apikey": api_key,
        "geocode": f"{long},{lat}",
        "format": "json",
        "lang": "ru_RU",
    }
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None
    json_response = (response.json())["response"]["GeoObjectCollection"][
        "featureMember"
    ][0]["GeoObject"]
    print(response.json())
    full_adress = json_response["metaDataProperty"]["GeocoderMetaData"]["text"]
    try:
        adress_index = json_response["metaDataProperty"]["GeocoderMetaData"]["Address"][
            "postal_code"
        ]
        return full_adress, adress_index
    except KeyError:
        print("Ошибка запроса")
        return full_adress


def get_organization(adress, long, lat):
    search_api_server = "https://search-maps.yandex.ru/v1/"

    search_params = {
        "apikey": api_key_org,
        "lang": "ru_RU",
        "text": adress,
        "ll": f"{long},{lat}",
        "type": "biz",
        "spn": f"{0.01},{0.01}",
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print("Ошибка выполнения запроса")
        print("Http статус: ", response.status_code, "(", response.reason, ")")
        return None
    try:
        org_name = response.json()["features"][1]["properties"]["name"]
        org_type = response.json()["features"][1]["properties"]["CompanyMetaData"][
            "Categories"
        ][0]["name"]
        return f"{org_type} - {org_name}"
    except:
        return "Организаций нет"
