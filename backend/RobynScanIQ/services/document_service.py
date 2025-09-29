from RobynScanIQ.database.repository import (
    add_document,
    get_all_documents,
)
from RobynScanIQ.models.document_model import Document
from RobynScanIQ.tasks.tasks import answer_question_task, process_document_task


async def process_document(file_content: bytes, filename: str):
    task = process_document_task.delay(file_content, filename)
    return task.id


async def ask_question(doc_id: int, question: str):
    task = answer_question_task.delay(doc_id, question)
    return task.id


def list_documents(db):
    return get_all_documents(db)


def create_document(db, file_name: str, text_content: str = '') -> Document:
    """Cria um documento no banco usando os nomes corretos do modelo."""
    document = Document(
        file_name=file_name,
        text_content=text_content,
    )
    return add_document(db, document)
