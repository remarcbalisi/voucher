import configparser
import os
from flask import Blueprint, Flask, jsonify, request, render_template, send_from_directory
from flask_pymongo import PyMongo

# config = configparser.ConfigParser()
# config.read(os.path.abspath(os.path.join("mongo.ini")))
# app = Flask(__name__)
# app.config['MONGO_URI'] = config['PROD']['DB_URI']
# mongo = PyMongo(app)

APP_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(APP_DIR, 'static')
TEMPLATE_FOLDER = os.path.join(APP_DIR, 'templates')

voucher_web = Blueprint('voucher_web', 'voucher_web', static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)


@voucher_web.route('/')
def index():
    print('Request for index page received')
    return render_template('voucher/index.html')


@voucher_web.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(voucher_web.root_path, 'voucher/static/voucher'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
