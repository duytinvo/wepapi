import os
from typing import Union
import aiofiles
from datetime import datetime
from fastapi import UploadFile
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from webapp.apis.version1.route_login import get_current_user_from_token
from webapp.core.constant import DOWNLOAD_FOLDER, UPLOAD_FOLDER
from webapp.db.models.users import User
from webapp.db.repository.wdcould import create_new_doc
from webapp.db.repository.wdcould import delete_doc_by_id
from webapp.db.repository.wdcould import retreive_doc
from webapp.db.session import get_db
from webapp.func.wdcloud import WCgenerator
from webapp.schemas.wdcloud import DocCreate, ShowDoc

router = APIRouter()


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


@router.post("/create-doc/", response_model=ShowDoc)
def create_doc(
    doc: DocCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token),
):
    doc = create_new_doc(doc=doc, db=db, owner_id=current_user.id)
    return doc


@router.post("/upload-file/")
async def create_upload_file(in_file: Union[UploadFile, None] = None):
    if not in_file:
        return {"message": "No upload file sent"}
    else:
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        filename = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{in_file.filename}'
        async with aiofiles.open(os.path.join(UPLOAD_FOLDER, filename), 'wb') as out_file:
            content = await in_file.read()  # async read
            await out_file.write(content)  # async write
        return {"input_filename": in_file.filename, "output_filename": filename}


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
