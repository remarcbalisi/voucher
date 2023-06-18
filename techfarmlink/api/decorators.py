# decorator for verifying the JWT
import os
import sys
from functools import wraps

import jwt
from flask import request, jsonify, current_app

from techfarmlink.api.model.user import UserSchema
from techfarmlink.api.queries.user import get_user_by_id


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
            user = get_user_by_id(data['uuid'])
            user_schema = UserSchema()
            current_user = user_schema.load(user)
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                'message': 'Token is invalid.'
            }), 401
        # returns the current logged-in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated
