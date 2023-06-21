import configparser
import os
from flask import Blueprint, render_template, send_from_directory

APP_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_FOLDER = os.path.join(APP_DIR, 'static')
TEMPLATE_FOLDER = os.path.join(APP_DIR, 'templates')

captive_portal_web = Blueprint('captive_portal_web', 'captive_portal_web', url_prefix='/captive-portal',
                               static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER, static_url_path='/captive-portal')


@captive_portal_web.route('/')
def index():
    return render_template('captive_portal/index.html')


@captive_portal_web.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(captive_portal_web.root_path, 'captive_portal/static/voucher'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
