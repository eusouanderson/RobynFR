from robyn import Robyn

from RobynScanIQ.config.env import settings
from RobynScanIQ.controllers import document_controller

app = Robyn(__file__)


@app.get('/')
def main():
    """Rota raiz para verificar se o serviço está funcionando."""
    return {'message': 'Hello!'}


app.post('/documents')(document_controller.upload_document)
app.post('/documents/<int:doc_id>/question')(
    document_controller.question_document
)
app.get('/documents')(document_controller.get_documents)

app.start(
    port=settings.APP_PORT,
    host=settings.APP_HOST,
)
