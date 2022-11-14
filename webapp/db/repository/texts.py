from datetime import datetime

from sqlalchemy.orm import Session

from webapp.db.models.texts import Doc
from webapp.schemas.texts import DocCreate


def create_new_doc(doc: DocCreate, db: Session, owner_id: int):
    timestamp = datetime.now()
    doc_object = Doc(
        text=doc.text, caption=doc.caption, timestamp=timestamp, owner_id=owner_id
    )
    # doc_object = Doc(**doc.dict(),
    #                  owner_id=owner_id)
    db.add(doc_object)
    db.commit()
    db.refresh(doc_object)
    return doc_object


def retreive_doc(id: int, db: Session):
    item = db.query(Doc).filter(Doc.id == id).first()
    return item


def list_docs(db: Session):
    docs = db.query(Doc).all()
    return docs


def delete_doc_by_id(id: int, db: Session, owner_id):
    existing_doc = db.query(Doc).filter(Doc.id == id)
    if not existing_doc.first():
        return 0
    existing_doc.delete(synchronize_session=False)
    db.commit()
    return 1
