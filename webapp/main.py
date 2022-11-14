from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from webapp.apis.base import api_router
from webapp.core.config import settings
from webapp.db.base import Base
from webapp.db.session import engine
from webapp.db.utils import check_db_connected
from webapp.db.utils import check_db_disconnected
from webapp.webs.base import api_router as web_app_router


def include_router(app):
    app.include_router(api_router)
    app.include_router(web_app_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    configure_static(app)
    include_router(app)
    create_tables()
    return app


app = start_application()


@app.on_event("startup")
async def app_startup():
    await check_db_connected()


@app.on_event("shutdown")
async def app_shutdown():
    await check_db_disconnected()
