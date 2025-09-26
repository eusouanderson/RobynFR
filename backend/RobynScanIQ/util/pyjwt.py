from datetime import datetime, timedelta
from typing import Any, Optional

import jwt

SECRET_KEY = 'sua_chave_super_secreta'
ALGORITHM = 'HS256'


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta = timedelta(hours=1)
) -> str:
    """
    Cria um token JWT com payload fornecido e tempo de expiração.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict[str, Any]]:
    """
    Decodifica um token JWT.
    Retorna None se o token for inválido ou expirado.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
