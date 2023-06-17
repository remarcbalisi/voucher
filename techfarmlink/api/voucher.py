import uuid
from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_cors import CORS

from techfarmlink.api.utils import expect
from techfarmlink.db import add_voucher, get_unclaimed_vouchers

voucher_api_v1 = Blueprint('voucher_api_v1', 'voucher_api_v1', url_prefix='/api/v1/voucher')

CORS(voucher_api_v1)


@voucher_api_v1.route('/list', methods=['GET'])
def api_get_vouchers():

    return jsonify({'message': 'Success', 'vouchers': get_unclaimed_vouchers()})


@voucher_api_v1.route('/add', methods=["POST"])
#@jwt_required
def api_post_voucher():
    post_data = request.get_json()
    try:
        name = expect(post_data.get('name'), str, 'name')
        description = expect(post_data.get('description'), str, 'description')
        voucher_code = expect(post_data.get('voucher_code'), str, 'voucher_code')
        amount = expect(post_data.get('amount'), float, 'amount')
        time_minutes = expect(post_data.get('time_minutes'), int, 'time_minutes')

        success, message, resp = add_voucher(name, description, voucher_code, amount, time_minutes, datetime.now())
        if success:
            return jsonify({"message": message}), 200
        return jsonify({"message": message}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400
