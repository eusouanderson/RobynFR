# tasks.py
from typing import Optional

from celery import Celery
from sqlalchemy.orm import Session

from RobynScanIQ.config.env import settings
from RobynScanIQ.database.postgres import SessionLocal
from RobynScanIQ.helper.rag import answer_question
from RobynScanIQ.models.document_model import Document
from RobynScanIQ.services.ocr_service import extract_text

redis_url = (
    f'redis://'
    f'{settings.REDIS_USERNAME}:{settings.REDIS_PASSWORD}@'
    f'{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
)

celery_app = Celery(
    'tasks',
    broker=redis_url,
    backend=redis_url,
)


@celery_app.task
def process_document_task(file_content: bytes, file_name: str):
    """
    Tarefa que executa o OCR e salva no banco de dados.
    Esta função roda em um processo worker, não bloqueando a aplicação web.
    """
    print(f'Iniciando OCR para o arquivo: {file_name}')
    text = extract_text(file_content)

    db: Session = SessionLocal()
    try:
        doc = Document(file_name=file_name, text_content=text)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        print(f'Documento {doc.id} salvo com sucesso.')
        return {'id': doc.id, 'file_name': doc.file_name}
    finally:
        db.close()


@celery_app.task
def answer_question_task(doc_id: int, question: str):
    """
    Tarefa que busca o documento e usa o RAG para responder.
    Também roda em um worker.
    """
    print(f'Buscando resposta para a pergunta sobre o doc: {doc_id}')
    db: Session = SessionLocal()
    try:
        doc: Optional[Document] = (
            db.query(Document).filter(Document.id == doc_id).first()
        )
        if not doc:
            return {'error': 'Documento não encontrado'}

        answer = answer_question(doc.text_content, question)
        return {'answer': answer}
    finally:
        db.close()
