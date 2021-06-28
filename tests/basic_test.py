import unittest
from flask import Flask

import sys

from werkzeug.wrappers import PlainRequest
sys.path.append(".")
# blueprint import
from app import create_app
import json

class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_find_distance(self):
        user_payload = json.dumps({"address": "New York"})
        response = self.app.post('/finddistance', headers={"Content-Type": "application/json"}, data=user_payload)
        data = json.loads(response.data)
        self.assertEqual(str, type(data['distance']))
        self.assertEqual(200, response.status_code)

    def test_bad_request(self):
        user_payload = json.dumps({"Addre": "asdkfalksdjflkasd"})
        response = self.app.post('/finddistance', headers={"Content-Type": "application/json"}, data=user_payload)
        self.assertEqual(400, response.status_code)

    def test_bad_address(self):
        user_payload = json.dumps({"address": "asdkfalksdjflkasd"})
        response = self.app.post('/finddistance', headers={"Content-Type": "application/json"}, data=user_payload)
        self.assertTrue(b"Nothing found" in response.data)

    def test_address_in_MKAD(self):
        user_payload = json.dumps({"address": "mocow ring"})
        response = self.app.post('/finddistance', headers={"Content-Type": "application/json"}, data=user_payload)
        data = json.loads(response.data)
        self.assertEqual("0.0(miles)", data["distance"])

if __name__ == '__main__':
    unittest.main()