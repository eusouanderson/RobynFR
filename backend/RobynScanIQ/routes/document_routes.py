from RobynScanIQ.controllers import document_controller


def register_document_routes(app):
    app.post('/documents')(document_controller.upload_document)
    app.post('/documents/<int:doc_id>/question')(
        document_controller.question_document
    )
    app.get('/documents')(document_controller.get_documents)
