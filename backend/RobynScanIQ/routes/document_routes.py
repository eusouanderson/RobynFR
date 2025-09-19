from robyn import Robyn, Request
from RobynScanIQ.helper.response_json import json_response
from RobynScanIQ.tasks.tasks import process_document_task, answer_question_task 

router = Robyn(__file__)

@router.post("/")
async def upload_document(request: Request):
    files = request.files
    if not files:
        return json_response({"detail": "Nenhum arquivo enviado"}, status=400)

    filename, content = list(files.items())[0]

    task = process_document_task.delay(content, filename)
    
    return json_response(
        {"message": "O documento foi recebido e está sendo processado.", "task_id": task.id},
        status=202 
    )


@router.post("/{doc_id}/question")
async def ask_question(request: Request):
    doc_id = int(request.path_params["doc_id"])
    form_data = await request.form()
    question = form_data.get("question")

    if not question:
        return json_response({"detail": "Pergunta não fornecida"}, status=400)

    task = answer_question_task.delay(doc_id, question)
    
    return json_response(
        {"message": "Sua pergunta está sendo processada.", "task_id": task.id},
        status=202
    )