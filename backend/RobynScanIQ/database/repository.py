import json
from sqlalchemy.orm import Session

from RobynScanIQ.database.redis import RedisConnection
from RobynScanIQ.models.document_model import Document
from RobynScanIQ.models.ia_response_model import IAResponse
from RobynScanIQ.helper.rag import answer_question

redis = RedisConnection()

# --- Documentos ---
def get_all_documents(db: Session):
    """Retorna todos os documentos, com cache no Redis."""
    cache_key = 'all_documents'
    cached = redis.get(cache_key)
    if cached:
        return [Document(**doc) for doc in json.loads(cached)]

    documents = db.query(Document).all()
    redis.set(cache_key, json.dumps([doc.to_dict() for doc in documents]))
    return documents

def get_document_by_id(db: Session, doc_id: int):
    """Retorna um documento pelo ID, com cache no Redis."""
    cache_key = f'document:{doc_id}'
    cached = redis.get(cache_key)
    if cached:
        return Document(**json.loads(cached))

    document = db.query(Document).filter(Document.id == doc_id).first()
    if document:
        redis.set(cache_key, json.dumps(document.to_dict()))
    return document

def add_document(db: Session, document: Document, question: str = 'Me diga o conteúdo deste documento com no máximo 50 palavras'):
    """Adiciona um novo documento ao banco, atualiza cache e processa IA se question fornecida."""
    db.add(document)
    db.commit()
    db.refresh(document)

    # Atualiza cache
    cache_key = f'document:{document.id}'
    redis.set(cache_key, json.dumps(document.to_dict()))
    redis.delete('all_documents')

    # Processa IA se houver pergunta
    ia_response = None
    if question:
        answer = answer_question(document.text_content, question)
        ia_response = IAResponse(
            question=question,
            answer=answer,
            document_id=document.id
        )
        db.add(ia_response)
        db.commit()
        db.refresh(ia_response)

    return document, ia_response


# --- Respostas da IA ---
def ask_and_save(db: Session, document_id: int, question: str):
    """Faz a pergunta e salva a resposta no banco (sem Redis)."""
    document = get_document_by_id(db, document_id)
    if not document:
        raise ValueError(f"Documento {document_id} não encontrado")

    answer = answer_question(document.text_content, question)

    ia_response = IAResponse(
        question=question,
        answer=answer,
        document_id=document.id 
    )
    db.add(ia_response)
    db.commit()
    db.refresh(ia_response)

    return ia_response

def get_ia_response_by_id(db: Session, response_id: int):
    """Retorna uma resposta da IA pelo ID (sem Redis)."""
    ia_response = db.query(IAResponse).filter(IAResponse.id == response_id).first()
    return ia_response

def get_all_ia_responses(db: Session):
    """Retorna todas as respostas da IA (sem Redis)."""
    responses = db.query(IAResponse).all()
    return responses
