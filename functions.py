from functools import wraps

import jwt
from flask import request
from playhouse.shortcuts import model_to_dict

from config import SECRET_KEY
from models import User
from responses import *


def advertisement_render(advertisement):
    return {**model_to_dict(advertisement), "user": advertisement.user.id}


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("jwt_token")

        if not token:
            return error_auth_req()
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        current_user = User.select().where(User.public_id == data["public_id"]).dicts()
        if not current_user:
            return error_auth_req()

        return f(current_user.get(), *args, **kwargs)

    return decorated
