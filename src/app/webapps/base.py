from fastapi import APIRouter

from app.webapps.login import route_login
from app.webapps.signup import route_signup

api_router = APIRouter()
api_router.include_router(route_signup.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
