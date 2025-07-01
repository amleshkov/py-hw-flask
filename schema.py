from pydantic import BaseModel


class UserSchema(BaseModel):
    login: str
    email: str
    password: str


class AdvertisementSchema(BaseModel):
    title: str
    description: str
    user: int
