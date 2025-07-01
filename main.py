from flask import Flask, request
from flask.views import MethodView
from playhouse.shortcuts import model_to_dict
from pydantic import ValidationError

from models import Advertisement, User, db
from responses import *
from schema import AdvertisementSchema, UserSchema


def advertisement_render(advertisement):
    return {**model_to_dict(advertisement), "user": advertisement.user.id}


class AdvertisementView(MethodView):
    @staticmethod
    def get():
        advertisements = list(Advertisement.select().dicts())
        return ok_with_data(advertisements)

    @staticmethod
    def post():
        data = request.json
        try:
            validated_data = AdvertisementSchema(**data)
        except ValidationError:
            return error_bad_request()
        advertisement = Advertisement(**validated_data.model_dump())
        advertisement.save()
        return ok_created(advertisement_render(advertisement))


class AdvertisementViewItem(MethodView):
    @staticmethod
    def get(item_id):
        query = Advertisement.select().where(Advertisement.id == item_id)
        if query.exists():
            advertisement = query.get()
            return ok_with_data(advertisement_render(advertisement))
        return error_not_found()

    @staticmethod
    def delete(item_id):
        query = Advertisement.select().where(Advertisement.id == item_id)
        if query.exists():
            query = Advertisement.delete().where(Advertisement.id == item_id)
            query.execute()
            return ok_deleted()
        return error_not_found()


def main():
    db.connect()
    db.create_tables([User, Advertisement])
    app = Flask("app")
    app.add_url_rule(
        "/ad",
        view_func=AdvertisementView.as_view("Advertisements"),
        methods=["GET", "POST"],
    )
    app.add_url_rule(
        "/ad/<int:item_id>",
        view_func=AdvertisementViewItem.as_view("Advertisement"),
        methods=["GET", "DELETE"],
    )
    app.run(host="localhost", port=5000, debug=True)


if __name__ == "__main__":
    admin = User(
        login="admin",
        email="admin@null.nl",
        password="$2b$12$57c1HWlejF/3NRHqhtBsGOKBGStgCVhuXe5cwWbVtDkY4qhk3Vque",
    )
    #    admin.save()
    main()
