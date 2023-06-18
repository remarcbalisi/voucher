from techfarmlink.api.model.user import UserSchemaStore
from techfarmlink.db import db


def get_user_by_email(email):
    try:
        user = list(db.users.find({"email": {"$eq": email}}))
        if user:
            return user[0]
        return False
    except Exception as e:
        return {}


def get_user_by_id(user_id):
    try:
        user = list(db.users.find({"_id": {"$eq": user_id}}))
        if user:
            return user[0]
        return False
    except Exception as e:
        return {}


def add_user(user: UserSchemaStore):

    exist = get_user_by_email(user.email)
    if exist:
        return False, f'User {user.email} already exist', exist

    return True, f'Successfully added {user.email}', db.users.insert_one(user.__dict__)
