from datetime import datetime
import uuid

from bson import ObjectId
from marshmallow import Schema, fields, post_load, pre_load
from werkzeug.security import generate_password_hash


class User(object):
    def __init__(self, name, email, phone_number, password, status='active', _id=None, email_verified=False, phone_number_verified=False, created_at=None):
        self._id = _id or uuid.uuid4().hex
        self.name = name
        self.email = email
        self.email_verified = email_verified
        self.phone_number = phone_number
        self.phone_number_verified = phone_number_verified
        self.password = password
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = status

    def __repr__(self):
        return '<User(name={self.name!r})>'.format(self=self)


class UserSchema(Schema):
    _id = fields.Str()
    name = fields.Str()
    email = fields.Str()
    email_verified = fields.Boolean()
    phone_number = fields.Str()
    phone_number_verified = fields.Boolean()
    password = fields.Str()
    created_at = fields.DateTime()
    status = fields.Str()

    @post_load
    def make_store(self, data, **kwargs):
        return User(**data)

    @pre_load
    def pre_process_details(self, data, **kwarg):
        data['_id'] = str(data['_id']) if isinstance(data['_id'], ObjectId) else data['_id']
        data['created_at'] = data['created_at'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(data['created_at'], datetime) else data['created_at']
        return data


class UserSchemaStore(Schema):
    name = fields.Str()
    email = fields.Str()
    phone_number = fields.Str()
    password = fields.Str()

    @post_load
    def make_store(self, data, **kwargs):
        data['password'] = generate_password_hash(data['password'])
        return User(**data)


class UserLogin(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<UserLogin(username={self.username!r})>'.format(self=self)


class UserSchemaLogin(Schema):
    username = fields.Str()
    password = fields.Str()

    @post_load
    def make_store(self, data, **kwargs):
        return UserLogin(**data)
