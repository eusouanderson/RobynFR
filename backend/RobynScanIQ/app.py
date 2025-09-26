from robyn import Robyn

from RobynScanIQ.config.env import settings
from RobynScanIQ.routes import document_routes

app = Robyn(__file__)


@app.get('/')
def main():
    """app.py main route"""
    return {'message': 'Hello!'}


app.post('/documents')(document_routes.upload_document)
app.post('/documents/<int:doc_id>/question')(document_routes.ask_question)

app.start(
    port=settings.APP_PORT,
    host=settings.APP_HOST,
)
