from robyn import Response
import json

def json_response(body: dict, *, status: int = 200, headers: dict | None = None):
    response_headers = {"Content-Type": "application/json"}
    if headers:
        response_headers.update(headers)

    return Response(
        body=json.dumps(body),  
        status_code=status,
        headers=response_headers
    )
