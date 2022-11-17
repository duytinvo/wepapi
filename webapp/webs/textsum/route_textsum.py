import os
import io
import aiohttp
import aiofiles
from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.responses import Response
from fastapi import responses
from fastapi import status
from fastapi.responses import FileResponse
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from webapp.apis.version1.route_login import get_current_user_from_token
from webapp.core.constant import DOWNLOAD, UPLOAD
from webapp.core.constant import DOWNLOAD_FOLDER, UPLOAD_FOLDER
from webapp.db.models.users import User
from webapp.db.repository.texts import create_new_doc
from webapp.db.repository.texts import list_docs
from webapp.db.repository.texts import retreive_doc
from webapp.db.session import get_db
from webapp.func.objdet_onnx import predict_object
from webapp.schemas.texts import DocCreate
from webapp.webs.texts.forms import DocCreateForm

templates = Jinja2Templates(directory="templates")
router = APIRouter(include_in_schema=False)

@router.get("/post-textsum/")
def create_textsum_get(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("textsum/create_textsum.html", {"request": request})


# @router.route("/upload_url", methods = ["GET"])
# async def upload_url(request):
#     try:
#         url = request.query_params["url"]
#         if not os.path.exists(UPLOAD_FOLDER):
#             os.mkdir(UPLOAD_FOLDER)
#         timestamp = datetime.now()
#         basename = os.path.basename(url)
#         filename = f'{timestamp.strftime("%Y%m%d_%H%M%S")}_{basename}'
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 content = await response.read()  # async read
#                 async with aiofiles.open(filepath, 'wb') as out_file:
#                     await out_file.write(content)  # async write

#         downfilepath = os.path.join(DOWNLOAD_FOLDER, filename)
#         if request.query_params["objtype"] == "logo":
#             onnx_path = "static/assets/yolov7-tiny_logo.onnx"
#             class_path = "static/assets/classes_logo.txt"
#         else:
#             onnx_path = "static/assets/yolov7-tiny.onnx"
#             class_path = "static/assets/classes.txt"
#         predict_object(onnx_path = onnx_path,
#                     class_path = class_path,
#                     img_path = filepath,
#                     pred_img_path=downfilepath)
#         # return Response(content=bytes)
#         # return JSONResponse(content=jsonable_encoder(url))
#         # return FileResponse(downfilepath, filename=filename)
#         return templates.TemplateResponse("objects/detail.html",
#                                           {"request": request, "img_path": os.path.join(DOWNLOAD, filename)},)
#     except Exception as e:
#         print(e)
#         return templates.TemplateResponse("objects/create_object.html", request.form().__dict__)


# @router.route("/upload_file", methods = ["POST"])
# async def upload_file(request:Request):
#     data = await request.form()
#     try:
#         if not os.path.exists(UPLOAD_FOLDER):
#             os.mkdir(UPLOAD_FOLDER)
#         timestamp = datetime.now()
#         filename = f'{timestamp.strftime("%Y%m%d_%H%M%S")}_{data["file"].filename}'
#         filepath = os.path.join(UPLOAD_FOLDER, filename)
#         async with aiofiles.open(filepath, 'wb') as out_file:
#             content = await (data["file"].read())  # async read
#             await out_file.write(content)  # async write
        
#         downfilepath = os.path.join(DOWNLOAD_FOLDER, filename)
#         if data["objtype"] == "logo":
#             onnx_path = "static/assets/yolov7-tiny_logo.onnx"
#             class_path = "static/assets/classes_logo.txt"
#         else:
#             onnx_path = "static/assets/yolov7-tiny.onnx"
#             class_path = "static/assets/classes.txt"
#         predict_object(onnx_path = onnx_path,
#                        class_path = class_path,
#                        img_path = filepath,
#                        pred_img_path=downfilepath)
#         # return FileResponse(downfilepath, filename=filename)
#         # return JSONResponse(content=jsonable_encoder(data["file"]))
#         return templates.TemplateResponse("objects/detail.html",
#                                           {"request": request, "img_path": os.path.join(DOWNLOAD, filename)},)
#     except Exception as e:
#         print(e)
#         return templates.TemplateResponse("objects/create_object.html", request.form().__dict__)


# @router.get("/download/{file_path:path}")
# async def download_image(file_path: str):
#     filename = os.path.basename(file_path)
#     filepath = os.path.join(DOWNLOAD_FOLDER, filename)
#     return FileResponse(filepath, filename=filename)
