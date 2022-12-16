from flask import Flask
from firebase_admin import credentials, initialize_app


cred = credentials.Certificate("api/key.json")
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "1234fbavkivp"

    from .userAPI import userAPI

    app.register_blueprint(userAPI, url_prefix = '/user')

    return app