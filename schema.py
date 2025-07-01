from pydantic import BaseModel


class UserSchemaSignup(BaseModel):
    login: str
    email: str
    password: str


class UserSchemaLogin(BaseModel):
    email: str
    password: str


class AdvertisementSchema(BaseModel):
    title: str
    description: str
    user: int
