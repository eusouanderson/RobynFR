# main.py
from robyn import ALLOW_CORS, Robyn

from RobynScanIQ.config.env import settings
from RobynScanIQ.routes import document_routes, ia_response_routes

app = Robyn(__file__)


ALLOW_CORS(app, origins='*')


@app.get('/')
def main():
    return {'message': 'Hello!'}


document_routes.register_document_routes(app)
ia_response_routes.register_ia_routes(app)

app.start(
    port=settings.APP_PORT,
    host=settings.APP_HOST,
)
