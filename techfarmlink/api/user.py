import os
import sys

import jwt
from flask import Blueprint, request, jsonify, current_app
from flask_cors import CORS
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta

from techfarmlink.api.model.user import UserSchemaStore, UserSchemaLogin, UserSchema
from techfarmlink.api.queries.user import add_user, get_user_by_email
from techfarmlink.api.utils import check_valid_email

user_api_v1 = Blueprint('user_api_v1', 'user_api_v1', url_prefix='/api/v1/user')

CORS(user_api_v1)


@user_api_v1.route('/add', methods=["POST"])
def api_post_user():
    post_data = request.get_json()
    try:
        user_schema = UserSchemaStore()
        user_schema = user_schema.load(post_data)

        success, message, resp = add_user(user=user_schema)
        if success:
            return jsonify({"message": message}), 200
        return jsonify({"message": message}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@user_api_v1.route('/login', methods=['POST'])
def login():
    post_data = request.get_json()
    try:
        login_schema = UserSchemaLogin()
        login_schema = login_schema.load(post_data)

        if check_valid_email(login_schema.username):
            user_data = get_user_by_email(login_schema.username)
            if not user_data:
                user_schema = None
            else:
                user_schema = UserSchema()
                user_schema = user_schema.load(user_data)
        else:
            user_schema = None

        if not user_schema:
            return jsonify({'message': 'Could not verify'}), 401

        if check_password_hash(user_schema.password, login_schema.password):
            # generates the JWT Token
            token = jwt.encode({
                'uuid': user_schema._id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, current_app.config['SECRET_KEY'])

            return jsonify({'token': token}), 201
            # returns 403 if password is wrong
        return jsonify({'message': 'Wrong username or password'}), 401
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return jsonify({'error': str(e), 'message': '{} {} {}'.format(exc_type, fname, exc_tb.tb_lineno)}), 400
