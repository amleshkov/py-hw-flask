import uuid
from datetime import datetime, timedelta, timezone

from bcrypt import checkpw, gensalt, hashpw
from flask import Flask
from playhouse.shortcuts import model_to_dict
from pydantic import ValidationError

from functions import *
from models import Advertisement, db
from schema import AdvertisementSchema, UserSchemaLogin, UserSchemaSignup

app = Flask("app")


@app.route("/ad", methods=["GET"])
def get_all():
    advertisements = list(Advertisement.select().dicts())
    return ok_with_data(advertisements)


@app.route("/ad", methods=["POST"])
@token_required
def post(current_user):
    data = {**request.json, "user": current_user.get("id")}
    try:
        validated_data = AdvertisementSchema(**data)
    except ValidationError:
        return error_bad_request()
    advertisement = Advertisement(**validated_data.model_dump())
    advertisement.save()
    return ok_created(advertisement_render(advertisement))


@app.route("/ad/<int:item_id>", methods=["GET"])
def get(item_id):
    query = Advertisement.select().where(Advertisement.id == item_id)
    if query.exists():
        advertisement = query.get()
        return ok_with_data(advertisement_render(advertisement))
    return error_not_found()


@app.route("/ad/<int:item_id>", methods=["DELETE"])
@token_required
def delete(current_user, item_id):
    query = Advertisement.select().where(Advertisement.id == item_id)
    if query.exists():
        advertisement_user_id = query.get().user_id
        if advertisement_user_id == current_user.get("id"):
            query = Advertisement.delete().where(Advertisement.id == item_id)
            query.execute()
            return ok_deleted()
        return error_unauthorized()
    return error_not_found()


@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    try:
        validated_data = UserSchemaSignup(**data)
    except ValidationError:
        return error_bad_request()
    user_data = validated_data.model_dump()
    login = user_data.get("login")
    email = user_data.get("email")
    password = user_data.get("password")
    existing_user = User.select().where(User.email == email).dicts()
    if existing_user:
        return error_bad_request()
    hashed_pw = hashpw(password.encode(), gensalt())
    public_id = str(uuid.uuid4())
    user = User(
        login=login, email=email, password=hashed_pw.decode(), public_id=public_id
    )
    user.save()
    return ok_created({"login": login, "public_id": public_id})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    try:
        validated_data = UserSchemaLogin(**data)
    except ValidationError:
        return error_bad_request()
    user_data = validated_data.model_dump()
    email = user_data.get("email")
    password = user_data.get("password")
    user = User.select().where(User.email == email)
    if not user or not checkpw(password.encode(), user[0].password.encode()):
        return error_auth_req()
    token = jwt.encode(
        {
            "public_id": user[0].public_id,
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
        },
        SECRET_KEY,
        algorithm="HS256",
    )
    response = ok_with_data(data="login success", cookie=("jwt_token", token))
    return response


def main():
    db.connect()
    db.create_tables([User, Advertisement])
    app.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    main()
