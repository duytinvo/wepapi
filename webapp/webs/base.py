from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from webapp.db.session import get_db
from webapp.webs.auth import route_login
from webapp.webs.jobs import route_jobs
from webapp.webs.wdcloud import route_wdcloud
from webapp.webs.users import route_users
from webapp.webs.vision import route_objdet

templates = Jinja2Templates(directory="templates")

api_router = APIRouter(include_in_schema=False)


@api_router.get("/")
async def home(request: Request, db: Session = Depends(get_db), msg: str = None):
    return templates.TemplateResponse(
        "general_pages/index.html", {"request": request, "msg": msg}
    )


api_router.include_router(route_jobs.router, prefix="/jobs-webapp", tags=["jobs-webapp"])
api_router.include_router(route_users.router, prefix="", tags=["users-webapp"])
api_router.include_router(route_login.router, prefix="", tags=["auth-webapp"])
api_router.include_router(
    route_wdcloud.router, prefix="/wdcloud-webapp", tags=["wdcloud-webapp"]
)
api_router.include_router(
    route_objdet.router, prefix="/vision-webapp/objdet", tags=["vision-webapp_objdet"]
)
