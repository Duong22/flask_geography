from flask import Blueprint, request
from decimal import Decimal
from typing import Tuple
import json
from src.geocoder import YandexGeocoder

API_KEY = "8507fcb7-4e42-4537-80ed-3b77efa71f95"

yandex_geocoder = YandexGeocoder(API_KEY)

geocoder = Blueprint('geocoder', __name__)

@geocoder.route("/findaddress", methods=['POST'])
def find_address():
    rq = request.get_json()
    longitude = rq['longitude']
    latitude = rq['latitude']
    address = yandex_geocoder.find_address(Decimal(longitude), Decimal(latitude))
    print(address)
    return json.dumps({"address": str(address)})

@geocoder.route("/findcoordinates", methods=['POST'])
def find_coordinates():
    address = request.get_json()['address']
    coordinates = yandex_geocoder.find_coordinates("new york")
    print(coordinates)
    return json.dumps({"coordinates": str(coordinates)})

@geocoder.route("/finddistance", methods=['POST'])
def find_distance():
    address = request.get_json()['address']
    distance = yandex_geocoder.calculate_distance(address=address)
    # print(distance)
    distance = str(distance) + " miles"
    return json.dumps({"distance": distance})