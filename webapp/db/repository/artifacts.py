from datetime import datetime

from sqlalchemy.orm import Session

from webapp.db.models.artifacts import Artifact
from webapp.schemas.artifacts import ShowArtifact


def create_new_artifact(timestamp: datetime, filename: str, dtype:str, is_upload: bool, owner_id: int, db: Session):
    file_object = Artifact(timestamp=timestamp, filename=filename, dtype=dtype, is_upload=is_upload, owner_id=owner_id)
    db.add(file_object)
    db.commit()
    db.refresh(file_object)
    return file_object

