# tasks.py
from celery import Celery
from sqlalchemy.orm import Session
from RobynScanIQ.database.postgree import SessionLocal  # Importe a sessão diretamente
from RobynScanIQ.models.document_model import Document
from RobynScanIQ.services.ocr_service import extract_text
from RobynScanIQ.services.rag_service import answer_question

# Configure Celery para usar Redis
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Redis como broker
    backend="redis://localhost:6379/0"  # Redis para armazenar resultados
)

@celery_app.task
def process_document_task(file_content: bytes, file_name: str):
    """
    Tarefa que executa o OCR e salva no banco de dados.
    Esta função roda em um processo worker, não bloqueando a aplicação web.
    """
    print(f"Iniciando OCR para o arquivo: {file_name}")
    text = extract_text(file_content)

    db: Session = SessionLocal()
    try:
        doc = Document(file_name=file_name, text_content=text)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        print(f"Documento {doc.id} salvo com sucesso.")
        return {"id": doc.id, "file_name": doc.file_name}
    finally:
        db.close()


@celery_app.task
def answer_question_task(doc_id: int, question: str):
    """
    Tarefa que busca o documento e usa o RAG para responder.
    Também roda em um worker.
    """
    print(f"Buscando resposta para a pergunta sobre o doc: {doc_id}")
    db: Session = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            return {"error": "Documento não encontrado"}
        
        answer = answer_question(doc.text_content, question)
        return {"answer": answer}
    finally:
        db.close()
