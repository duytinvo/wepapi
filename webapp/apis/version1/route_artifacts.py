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
from webapp.db.repository.artifacts import create_new_artifact
# from webapp.db.repository.texts import delete_doc_by_id
# from webapp.db.repository.texts import retreive_doc
from webapp.db.session import get_db
from webapp.schemas.artifacts import ShowArtifact

router = APIRouter()


@router.post("/upload-artifact/", response_model=ShowArtifact)
async def create_upload_artifact(in_file: Union[UploadFile, None] = None,
                                 db: Session = Depends(get_db),
                                 current_user: User = Depends(get_current_user_from_token),):
    if not in_file:
        return {"message": "No upload file sent"}
    else:
        if not os.path.exists(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        timestamp = datetime.now()
        filename = f'{timestamp.strftime("%Y%m%d_%H%M%S")}_{in_file.filename}'
        dtype = "image"
        is_upload = True
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        async with aiofiles.open(filepath, 'wb') as out_file:
            content = await in_file.read()  # async read
            await out_file.write(content)  # async write
        
        file_object = create_new_artifact(timestamp=timestamp, filename=filename, 
                                          dtype=dtype, is_upload=is_upload, owner_id=current_user.id, db=db)
        return file_object
