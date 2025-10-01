from http import HTTPStatus

from robyn import Request

from RobynScanIQ.database.postgres import get_db
from RobynScanIQ.helper.response_json import json_response
from RobynScanIQ.services.ia_response_service import (
    ask_question_and_save,
    get_ia_response,
    list_ia_responses,
)


async def question_ia(request: Request):
    """Faz uma pergunta a uma IA sobre um documento."""
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

    task_id = await ask_question_and_save(doc_id, question)
    return json_response(
        {
            'message': 'Pergunta enviada para processamento.',
            'task_id': task_id,
        },
        status=HTTPStatus.ACCEPTED,
    )


async def get_all_ia_responses():
    """Retorna todas as respostas da IA no banco/cache."""
    responses_list = []
    for db in get_db():
        responses = list_ia_responses(db)
        responses_list = [
            r.to_dict() if hasattr(r, 'to_dict') else r for r in responses
        ]
    return json_response(
        {'ia_responses': responses_list},
        status=HTTPStatus.OK,
    )


async def get_ia_response_by_id_controller(request: Request):
    """Retorna uma resposta específica da IA pelo ID."""
    try:
        response_id = int(request.path_params['response_id'])
    except (KeyError, ValueError):
        return json_response(
            {'detail': 'ID da resposta inválido'},
            status=HTTPStatus.BAD_REQUEST,
        )

    response_data = None
    for db in get_db():
        response_data = get_ia_response(db, response_id)

    if not response_data:
        return json_response(
            {'detail': f'Resposta {response_id} não encontrada'},
            status=HTTPStatus.NOT_FOUND,
        )

    return json_response(
        {'ia_response': response_data.to_dict()},
        status=HTTPStatus.OK,
    )
