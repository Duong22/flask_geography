import unittest
from flask import Flask

import sys
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

if __name__ == '__main__':
    unittest.main()