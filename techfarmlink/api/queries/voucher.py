from techfarmlink.api.model.login_voucher import LoginVoucherSchema
from techfarmlink.db import db


def get_voucher_by_code(code):
    try:
        voucher = list(db.vouchers.find({"voucher_code": {"$eq": code}}))
        print(voucher)
        if voucher:
            return voucher[0]
        return False
    except Exception as e:
        return {}


def add_login_voucher(attempt_voucher: LoginVoucherSchema):

    exist = get_voucher_by_code(attempt_voucher.voucher_code_entered)
    if not exist:
        return False, f'Voucher {attempt_voucher.voucher_code_entered} Failed', exist

    if not exist['status'] == "unclaimed":
        return False, f'Voucher {attempt_voucher.voucher_code_entered} already claimed', exist

    return True, f'Successfully logged in {attempt_voucher.voucher_code_entered}', exist
