from flask import Blueprint, request
from decimal import Decimal
from typing import Tuple
import json

from src.geocoder import YandexGeocoder
from src.exceptions import InvalidKey

API_KEY = "8507fcb7-4e42-4537-80ed-3b77efa71f95"

yandex_geocoder = YandexGeocoder(API_KEY)

geocoder = Blueprint('geocoder', __name__)

@geocoder.route("/findaddress", methods=['POST'])
def find_address():
    try:
        rq = request.get_json()
        longitude = rq['longitude']
        latitude = rq['latitude']
    except:
        return "Bad request", 400

    try:
        address = yandex_geocoder.find_address(Decimal(longitude), Decimal(latitude))
        print(address)
        return json.dumps({"address": str(address)})
    except Exception as e:
        return str(e), 500

@geocoder.route("/findcoordinates", methods=['POST'])
def find_coordinates():
    try:
        address = request.get_json()["address"]
    except:
        return "Bad request, please use json formart", 400

    try:
        coordinates = yandex_geocoder.find_coordinates(address=address)
        print(coordinates)
        return json.dumps({"coordinates": str(coordinates)})
    except Exception as e:
        return str(e), 500

@geocoder.route("/finddistance", methods=['POST'])
def find_distance():
    try:
        address = request.get_json()['address']
    except:
        return "Bad request", 400

    try:
        distance = yandex_geocoder.calculate_distance(address=address)
        # print(distance)
        distance = str(distance) + "(miles)"
        return json.dumps({"distance": distance})
    except Exception as e:
        return str(e), 500