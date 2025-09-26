import json
from typing import Dict, Optional

from robyn import Response


def json_response(
    body: dict,
    *,
    status: int = 200,
    headers: Optional[Dict] = None,
):
    """Retorna um Response JSON padronizado."""
    response_headers = {'Content-Type': 'application/json'}
    if headers:
        response_headers.update(headers)

    return Response(
        description=json.dumps(body),
        status_code=status,
        headers=response_headers,
    )
