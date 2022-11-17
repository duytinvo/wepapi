from fastapi import APIRouter

from webapp.apis.version1 import route_jobs
from webapp.apis.version1 import route_login
from webapp.apis.version1 import route_wdcloud
from webapp.apis.version1 import route_users
from webapp.apis.version1 import route_artifacts

api_router = APIRouter()
api_router.include_router(route_users.router, prefix="/users", tags=["users"])
api_router.include_router(route_jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(route_login.router, prefix="/login", tags=["login"])
api_router.include_router(route_wdcloud.router, prefix="/wordcloud", tags=["wordcloud"])
api_router.include_router(route_artifacts.router, prefix="/files", tags=["files"])
