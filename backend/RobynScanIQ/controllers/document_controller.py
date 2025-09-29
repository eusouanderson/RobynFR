import os
import tempfile
from http import HTTPStatus

from robyn import Request

from RobynScanIQ.database.postgres import get_db
from RobynScanIQ.helper.response_json import json_response
from RobynScanIQ.services.document_service import (
    ask_question,
    create_document,
    list_documents,
    process_document,
)
from RobynScanIQ.util.pypdf import extract_pdf_text


async def upload_document(request: Request):
    """Recebe um arquivo PDF, extrai o texto e inicia
    o processamento assíncrono."""
    if not request.files:
        return json_response(
            {'detail': 'Nenhum arquivo enviado'},
            status=HTTPStatus.BAD_REQUEST,
        )

    filename, file_bytes = next(iter(request.files.items()))

    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    text_content = extract_pdf_text(tmp_path)
    os.remove(tmp_path)

    for db in get_db():
        create_document(db, filename, text_content=text_content)

    task_id = await process_document(file_bytes, filename)

    return json_response(
        {'message': 'Documento recebido.', 'task_id': task_id},
        status=HTTPStatus.ACCEPTED,
    )


async def question_document(request: Request):
    """Faz uma pergunta sobre um documento específico."""
    try:
        doc_id = int(request.path_params['doc_id'])
    except (KeyError, ValueError):
        return json_response(
            {'detail': 'ID do documento inválido'},
            status=HTTPStatus.BAD_REQUEST,
        )

    question = request.form_data.get('question')
    if not question:
        return json_response(
            {'detail': 'Pergunta não fornecida'},
            status=HTTPStatus.BAD_REQUEST,
        )

    task_id = await ask_question(doc_id, question)
    return json_response(
        {'message': 'Pergunta processada.', 'task_id': task_id},
        status=HTTPStatus.ACCEPTED,
    )


async def get_documents():
    """Retorna a lista de documentos no banco."""
    documents_list = []
    for db in get_db():
        documents = list_documents(db)
        documents_list = [
            doc.to_dict() if hasattr(doc, 'to_dict') else doc
            for doc in documents
        ]
    return json_response(
        {'documents': documents_list},
        status=HTTPStatus.OK,
    )
