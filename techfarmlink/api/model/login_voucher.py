from datetime import datetime
import uuid

from bson import ObjectId
from marshmallow import Schema, fields, post_load, pre_load


class LoginVoucher(object):
    def __init__(self, device_id, voucher_code_entered, points=0, status=None, _id=None, created_at=None):
        self._id = _id or uuid.uuid4().hex
        self.device_id = device_id
        self.voucher_code_entered = voucher_code_entered
        self.points = points
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return '<LoginVoucher(voucher_code_entered={self.voucher_code_entered!r})>'.format(self=self)


class LoginVoucherSchema(Schema):
    device_id = fields.Str()
    voucher_code_entered = fields.Str()
    points = fields.Float()
    status = fields.Str()

    @post_load
    def make_store(self, data, **kwargs):
        return LoginVoucher(**data)
