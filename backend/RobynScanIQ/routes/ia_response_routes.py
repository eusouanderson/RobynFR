from RobynScanIQ.controllers import ia_response_controller

def register_ia_routes(app):
    app.get("/ia/responses")(ia_response_controller.list_ia_responses)
    app.get("/ia/responses/<int:response_id>")(ia_response_controller.get_ia_response)
