import os
import configparser

from flask import Flask, render_template
# from flask.json import JSONEncoder
from json import JSONEncoder
from flask_cors import CORS
##from flask_bcrypt import Bcrypt
##from flask_jwt_extended import JWTManager

from bson import json_util, ObjectId
from datetime import datetime, timedelta

from techfarmlink.api.user import user_api_v1
from techfarmlink.api.voucher import voucher_api_v1
from techfarmlink.voucher.index import voucher_web


class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)


def create_app():

    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    TEMPLATE_FOLDER = os.path.join(APP_DIR, 'build/templates')

    app = Flask(__name__, static_folder=STATIC_FOLDER,
                template_folder=TEMPLATE_FOLDER,
                )
    # app.json_encoder = MongoJsonEncoder
    config = configparser.ConfigParser()
    config.read(os.path.abspath(os.path.join("mongo.ini")))
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = config['PROD']['DB_URI']
    app.config['SECRET_KEY'] = 'your secret key'

    CORS(app)

    app.register_blueprint(voucher_api_v1)
    app.register_blueprint(voucher_web)
    app.register_blueprint(user_api_v1)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve(path):
        return render_template('index.html')

    return app
