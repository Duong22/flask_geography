from flask import Blueprint, request
from decimal import Decimal
from src.geocoder import YandexGeocoder
import json

API_KEY = "8507fcb7-4e42-4537-80ed-3b77efa71f95"

yandex_geocoder = YandexGeocoder(API_KEY)

geocoder = Blueprint('geocoder', __name__)

@geocoder.route("/findaddress", methods = ['POST'])
def find_address():
    content = request.get_json()
    longitude = content["longitude"]
    latitude = content["latitude"]
    address = yandex_geocoder.find_address(Decimal(longitude), Decimal(latitude))
    print(address)
    return json.dumps({"address": address})

@geocoder.route("/findcoordinates",  methods = ['POST'])
def find_coordinates():
    content = request.get_json()
    address = content["address"]
    coordinates = yandex_geocoder.find_coordinates(address)
    print(coordinates)
    return str(coordinates)

@geocoder.route("/finddistance", methods = ['POST'])
def find_distance():
    content = request.get_json()
    address = content["address"]
    distance = yandex_geocoder.calculate_distance(address=address)
    print(distance)
    return str(distance)