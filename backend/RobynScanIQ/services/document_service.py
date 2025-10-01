from RobynScanIQ.database.repository import (
    add_document,
    get_all_documents,
)
from RobynScanIQ.models.document_model import Document
from RobynScanIQ.tasks.tasks import answer_question_task, process_document_task


async def process_document(file_content: bytes, filename: str):
    """Executa a task assíncrona que processa o documento e salva no banco."""
    task = process_document_task.delay(file_content, filename)
    return task.id


async def ask_question(doc_id: int, question: str):
    """Executa a task assíncrona que pergunta para a IA e salva a resposta no banco."""
    task = answer_question_task.delay(doc_id, question)
    return task.id


def list_documents(db):
    """Lista todos os documentos do banco/cache."""
    return get_all_documents(db)


def create_document(db, file_name: str, text_content: str = '') -> Document:
    document = Document(file_name=file_name, text_content=text_content)
    doc, _ = add_document(db, document) 
    return doc

