import contextlib
import os

import fastapi.responses
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app.database.base import Base
from app.database.session import engine
from app.database.utils import check_db_connected
from app.database.utils import check_db_disconnected
from app.webapps.base import api_router as web_app_router

app_dir = os.path.dirname(__file__)


def include_router(app):
    app.include_router(web_app_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory=f"{app_dir}/static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


@contextlib.asynccontextmanager
async def lifespan(app):
    await check_db_connected()
    yield
    await check_db_disconnected()


def start_application():
    app = FastAPI(title="FastAPI-2FA", lifespan=lifespan)
    app.templates = Jinja2Templates(directory=f"{app_dir}/templates")
    include_router(app)
    configure_static(app)
    create_tables()
    return app


app = start_application()


@app.get("/")
async def root():
    return fastapi.responses.RedirectResponse(url="/signup/")
