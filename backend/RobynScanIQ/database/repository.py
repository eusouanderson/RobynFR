import json

from sqlalchemy.orm import Session

from RobynScanIQ.database.redis import RedisConnection
from RobynScanIQ.models.document_model import Document

redis = RedisConnection()


def get_all_documents(db: Session):
    cache_key = 'all_documents'
    cached = redis.get(cache_key)
    if cached:
        return [Document(**doc) for doc in json.loads(cached)]

    documents = db.query(Document).all()

    redis.set(cache_key, json.dumps([doc.to_dict() for doc in documents]))
    return documents


def get_document_by_id(db: Session, doc_id: int):
    cache_key = f'document:{doc_id}'
    cached = redis.get(cache_key)
    if cached:
        return Document(**json.loads(cached))

    document = db.query(Document).filter(Document.id == doc_id).first()
    if document:
        redis.set(cache_key, json.dumps(document.to_dict()))
    return document


def add_document(db: Session, document: Document):
    db.add(document)
    db.commit()
    db.refresh(document)

    cache_key = f'document:{document.id}'
    redis.set(cache_key, json.dumps(document.to_dict()))
    redis.delete('all_documents')
    return document
