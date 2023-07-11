from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_cors import CORS

from techfarmlink.api.decorators import token_required
from techfarmlink.api.model.login_voucher import LoginVoucherSchema
from techfarmlink.api.queries.voucher import add_login_voucher
from techfarmlink.api.utils import expect
from techfarmlink.db import add_voucher, get_unclaimed_vouchers

voucher_api_v1 = Blueprint('voucher_api_v1', 'voucher_api_v1', url_prefix='/api/v1/voucher')

CORS(voucher_api_v1)


@voucher_api_v1.route('/list', methods=['GET'])
@token_required
def api_get_vouchers(current_user):

    return jsonify({'message': 'Success', 'vouchers': get_unclaimed_vouchers()})


@voucher_api_v1.route('/add', methods=["POST"])
@token_required
def api_post_voucher(current_user):
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


@voucher_api_v1.route('/login', methods=["POST"])
def api_claim_voucher():
    post_data = request.get_json()
    try:
        voucher_code_entered = expect(post_data.get('voucher_code_entered'), str, 'voucher_code_entered')
        device_id = expect(post_data.get('device_id'), str, 'device_id')

        login_voucher_schema = LoginVoucherSchema()
        success, message, resp = add_login_voucher(login_voucher_schema.load(post_data))
        if success:
            return jsonify({"message": message}), 200
        return jsonify({"message": message}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 400
