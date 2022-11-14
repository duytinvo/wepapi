import os

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.responses import FileResponse
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from webapp.apis.version1.route_login import get_current_user_from_token
from webapp.core.constant import DOWNLOAD
from webapp.core.constant import DOWNLOAD_FOLDER
from webapp.db.models.users import User
from webapp.db.repository.texts import create_new_doc
from webapp.db.repository.texts import list_docs
from webapp.db.repository.texts import retreive_doc
from webapp.db.session import get_db
from webapp.func.texts import WCgenerator
from webapp.schemas.texts import DocCreate
from webapp.webs.texts.forms import DocCreateForm

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)


@router.get("/wordcloudboard/")
async def wordcloudboard(
    request: Request, db: Session = Depends(get_db), msg: str = None
):
    docs = list_docs(db=db)
    # filenames = ['{doc.owner_id}_{doc.id}_{doc.timestamp.strftime("%Y%m%d_%H%M%S")}.jpg' for doc in docs]
    return templates.TemplateResponse(
        "texts/wordcloudboard.html", {"request": request, "docs": docs, "msg": msg}
    )


@router.get("/download/{file_path:path}")
async def download_wordcloud(file_path: str):
    filename = os.path.basename(file_path)
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    return FileResponse(filepath, filename=filename)


@router.get("/details/{id}")
def doc_detail(id: int, request: Request, db: Session = Depends(get_db)):
    doc = retreive_doc(id=id, db=db)
    filename = f'{doc.owner_id}_{doc.id}_{doc.timestamp.strftime("%Y%m%d_%H%M%S")}.jpg'
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    text = doc.text
    _ = WCgenerator.save_wc(text, filename=filepath)
    return templates.TemplateResponse(
        "texts/detail.html",
        {"request": request, "doc": doc, "img_path": os.path.join(DOWNLOAD, filename)},
    )


@router.get("/post-a-doc/")
def create_doc_get(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("texts/create_text.html", {"request": request})


@router.post("/post-a-doc/")
async def create_doc_post(request: Request, db: Session = Depends(get_db)):
    form = DocCreateForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            token = request.cookies.get("access_token")
            scheme, param = get_authorization_scheme_param(
                token
            )  # scheme will hold "Bearer" and param will hold actual token value
            current_user: User = get_current_user_from_token(token=param, db=db)
            doc = DocCreate(**form.__dict__)
            doc = create_new_doc(doc=doc, db=db, owner_id=current_user.id)
            return responses.RedirectResponse(
                f"/texts-webapp/details/{doc.id}", status_code=status.HTTP_302_FOUND
            )
        except Exception as e:
            print(e)
            form.__dict__.get("errors").append(
                "You might not be logged in, In case problem persists please contact us."
            )
            return templates.TemplateResponse("texts/create_text.html", form.__dict__)
    return templates.TemplateResponse("texts/create_text.html", form.__dict__)


@router.get("/delete-doc/")
def show_jobs_to_delete(request: Request, db: Session = Depends(get_db)):
    docs = list_docs(db=db)
    return templates.TemplateResponse(
        "texts/show_texts_to_delete.html", {"request": request, "docs": docs}
    )
