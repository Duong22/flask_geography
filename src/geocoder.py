from flask import Blueprint 
from decimal import Decimal
from typing import Tuple
import requests
import json

from math import sin, cos, sqrt, atan2, radians

# from .exceptions import InvalidKey, NothingFound, UnexpectedResponse

API_KEY = "8507fcb7-4e42-4537-80ed-3b77efa71f95"

class YandexGeocoder(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.long_moscow_ring_road, self.lat_moscow_ring_road = self.find_coordinates(address="Moscow Ring Road")
    
    def request_geocoder(self, location):
        response = requests.get(
            "https://geocode-maps.yandex.ru/1.x/",
            params=dict(format="json", apikey=self.api_key, geocode=location, lang='en_RU'),
        )

        if response.status_code == 200:
            return response.json()["response"]
        # elif response.status_code == 400:
        #     raise InvalidKey()
        # else:
        #     raise UnexpectedResponse(
        #         f"status_code={response.status_code}, body={response.content}"
        #     )

    def find_coordinates(self, address=None) -> Tuple[Decimal]:
        data = self.request_geocoder(address)["GeoObjectCollection"]["featureMember"]

        # if not data:
            # raise NothingFound(f'Nothing found for "{address}"')

        coordinates = data[0]["GeoObject"]["Point"]["pos"]  # type: str
        longitude, latitude = tuple(coordinates.split(" "))

        return Decimal(longitude), Decimal(latitude)

    def find_address(self, longitude=None, latitude=None) -> str:
        coordinates = str(longitude) + ',' + str(latitude)
        data = self.request_geocoder(coordinates)["GeoObjectCollection"]["featureMember"]

        # if not data:
            # raise NothingFound(f'Nothing found for "{longitude}, {latitude}"')
        
        return data[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]

    def calculate_distance(self, longitude=None, latitude=None, address=None):
        if address is not None:
            longitude, latitude = self.find_coordinates(address)
        
        R = 6373.0

        lat1 = radians(self.lat_moscow_ring_road)
        lon1 = radians(self.long_moscow_ring_road)
        lat2 = radians(latitude)
        lon2 = radians(longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

yandex_geocoder = YandexGeocoder(API_KEY)

geocoder = Blueprint('geocoder', __name__)

@geocoder.route("/findaddress")
def find_address():
    address = yandex_geocoder.find_address(Decimal("37.587093"), Decimal("55.733969"))
    print(address)
    return json.dumps({"address": address})

@geocoder.route("/findcoordinates")
def find_coordinates():
    coordinates = yandex_geocoder.find_coordinates("new york")
    print(coordinates)
    return str(coordinates)

@geocoder.route("/finddistance")
def find_distance():
    distance = yandex_geocoder.calculate_distance(address="New york")
    print(distance)
    return str(distance)