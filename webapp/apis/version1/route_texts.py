import os

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from webapp.apis.version1.route_login import get_current_user_from_token
from webapp.core.constant import DOWNLOAD_FOLDER
from webapp.db.models.users import User
from webapp.db.repository.texts import create_new_doc
from webapp.db.repository.texts import delete_doc_by_id
from webapp.db.repository.texts import retreive_doc
from webapp.db.session import get_db
from webapp.func.texts import WCgenerator
from webapp.schemas.texts import DocCreate

router = APIRouter()
# templates = Jinja2Templates(directory="templates")


@router.post(
    "/generate-wordcloud/",
    responses={
        200: {
            "description": "A wordcloud of given text",
            "content": {"image/jpeg": {"example": "No example available."}},
        }
    },
)
def generate_wordcloud(
    doc: DocCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    doc = create_new_doc(doc=doc, db=db, owner_id=current_user.id)
    filename = (
        f'{current_user.id}_{doc.id}_{doc.timestamp.strftime("%Y%m%d_%H%M%S")}.jpg'
    )
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.mkdir(DOWNLOAD_FOLDER)
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    text = doc.text
    _ = WCgenerator.save_wc(text, filename=filepath)
    return FileResponse(filepath, filename=filename)


@router.delete("/delete/{id}")
def delete_doc(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    doc = retreive_doc(id=id, db=db)
    if not doc:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Doc with id {id} does not exist",
        )
    print(doc.owner_id, current_user.id, current_user.is_superuser)
    if doc.owner_id == current_user.id or current_user.is_superuser:
        filename = (
            f'{current_user.id}_{doc.id}_{doc.timestamp.strftime("%Y%m%d_%H%M%S")}.jpg'
        )
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        delete_doc_by_id(id=id, db=db, owner_id=current_user.id)
        return {"detail": "Successfully deleted."}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not permitted!!!!"
    )
