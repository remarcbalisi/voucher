from datetime import datetime
import uuid

from bson import ObjectId
from marshmallow import Schema, fields, post_load, pre_load


class Voucher(object):
    def __init__(self, name, description, voucher_code, amount, time_minutes, status, _id=None, created_at=None):
        self._id = _id or uuid.uuid4().hex
        self.name = name
        self.description = description
        self.voucher_code = voucher_code
        self.amount = amount
        self.time_minutes = time_minutes
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = status

    def __repr__(self):
        return '<Voucher(name={self.name!r})>'.format(self=self)


class VoucherSchema(Schema):
    _id = fields.Str()
    name = fields.Str()
    description = fields.Str()
    voucher_code = fields.Str()
    amount = fields.Number()
    time_minutes = fields.Number()
    created_at = fields.DateTime()
    status = fields.Str()

    @post_load
    def make_store(self, data, **kwargs):
        return Voucher(**data)

    @pre_load
    def pre_process_details(self, data, **kwarg):
        data['_id'] = str(data['_id']) if isinstance(data['_id'], ObjectId) else data['_id']
        data['created_at'] = data['created_at'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(data['created_at'], datetime) else data['created_at']
        return data
