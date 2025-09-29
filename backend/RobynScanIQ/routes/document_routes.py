from http import HTTPStatus

from robyn import Request, Robyn

from RobynScanIQ.helper.response_json import json_response
from RobynScanIQ.tasks.tasks import answer_question_task, process_document_task

router = Robyn(__file__)


@router.post('/')
async def upload_document(request: Request):
    """Endpoint to upload a document."""

    if not request.files:
        return json_response(
            {'detail': 'Nenhum arquivo enviado'}, status=HTTPStatus.BAD_REQUEST
        )

    filename, content = next(iter(request.files.items()))
    task = process_document_task.delay(content, filename)

    return json_response(
        {
            'message': 'O documento foi recebido e está sendo processado.',
            'task_id': task.id,
        },
        status=HTTPStatus.ACCEPTED,
    )


@router.post('/{doc_id}/question')
async def ask_question(request: Request):
    """Endpoint to ask a question about a document."""

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

    task = answer_question_task.delay(doc_id, question)

    return json_response(
        {
            'message': 'Sua pergunta está sendo processada.',
            'task_id': task.id,
        },
        status=HTTPStatus.ACCEPTED,
    )
