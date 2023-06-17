from flask import Blueprint, request, jsonify
from flask_cors import CORS

from techfarmlink.api.model.user import UserSchemaStore
from techfarmlink.api.queries.user import add_user

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
