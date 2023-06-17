import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo

from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId

from techfarmlink.api.model.voucher import TransactionSchema, Voucher


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "techfarmlink", None)

    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def get_unclaimed_vouchers():
    try:
        loaded_objects = db.vouchers.find(
            {"status": {"$eq": 'unclaimed'}}
        )
        new_objects = []
        for loaded_object in loaded_objects:
            voucher_schema = TransactionSchema()
            new_objects.append(voucher_schema.load(loaded_object).__dict__)
        return new_objects

    except Exception as e:
        print(e)
        return []


def get_voucher_by_code(voucher_code):
    try:
        return db.vouchers.find({"voucher_code": {"$eq": voucher_code}})

    except (StopIteration) as _:

        return None

    except Exception as e:
        return {}


def add_voucher(name, description, voucher_code, amount, time_minutes, date):

    exist = get_voucher_by_code(voucher_code)
    if exist:
        return False, f'Voucher {voucher_code} already exist', exist

    voucher_doc = {'name': name, 'description': description, 'voucher_code': voucher_code, 'amount': amount,
                   'time_minutes': time_minutes, 'created_at': date, 'status': 'unclaimed'}  # unclaimed, claimed, expired

    return True, f'Successfully added {voucher_code}', db.vouchers.insert_one(voucher_doc)
