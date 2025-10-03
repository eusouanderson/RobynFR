import json
from typing import Any, Dict, Optional

from robyn import Response


def json_response(
    body: Dict[str, Any],
    *,
    status: int = 200,
    headers: Optional[Dict[str, str]] = None,
):
    """Retorna um Response JSON padronizado."""
    response_headers = {'Content-Type': 'application/json'}
    if headers:
        response_headers.update(headers)

    return Response(
        description=json.dumps(body, ensure_ascii=False),
        status_code=status,
        headers=response_headers,
    )
