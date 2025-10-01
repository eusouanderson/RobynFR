from RobynScanIQ.database.postgres import get_db
from RobynScanIQ.database.repository import (
    get_all_ia_responses,
    get_ia_response_by_id,
)
from RobynScanIQ.models.ia_response_model import IAResponse
from RobynScanIQ.tasks.tasks import answer_question_task


async def ask_question_and_save(doc_id: int, question: str):
    """
    Executa a task assíncrona que pergunta para a IA e salva a resposta
    no banco (via Celery ou outro worker).
    Retorna o ID da task.
    """
    task = answer_question_task.delay(doc_id, question)
    return task.id


def list_ia_responses() -> list[IAResponse]:
    """Lista todas as respostas de IA do banco/cache."""
    db = next(get_db())
    try:
        return get_all_ia_responses(db)
    finally:
        db.close()


def get_ia_response(response_id: int) -> IAResponse:
    """Retorna uma resposta específica de IA pelo ID."""
    db = next(get_db())
    try:
        return get_ia_response_by_id(db, response_id)
    finally:
        db.close()
