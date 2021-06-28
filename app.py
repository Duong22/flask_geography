import os
from flask import Flask

# blueprint import
from src.route import geocoder

def create_app():
    app = Flask(__name__)   
    # register blueprint
    app.register_blueprint(geocoder)
    return app


if __name__ == "__main__":
    create_app().run(debug=True, host='0.0.0.0', port=5002)
