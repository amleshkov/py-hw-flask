from datetime import datetime

from peewee import (CharField, DateTimeField, ForeignKeyField, Model,
                    PostgresqlDatabase, TextField)

from config import *

db = PostgresqlDatabase(
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
)


class User(Model):
    login = CharField(max_length=64, null=False, unique=True)
    email = CharField(max_length=255, null=False, unique=True)
    password = CharField(max_length=60, null=False)

    class Meta:
        database = db


class Advertisement(Model):
    title = CharField(max_length=255, null=False)
    description = TextField(null=False)
    created = DateTimeField(default=datetime.now())
    user = ForeignKeyField(User, backref="advertisements")

    class Meta:
        database = db
