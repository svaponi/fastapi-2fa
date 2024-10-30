from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    secret: str


class ShowUser(BaseModel):
    email: str
