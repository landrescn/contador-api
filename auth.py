import os
from fastapi import Header, HTTPException, status

API_TOKEN = os.getenv("API_TOKEN")


def require_token(authorization: str | None = Header(default=None)):
    # Si no hay token configurado en el entorno, dejamos pasar (útil para pruebas)
    if not API_TOKEN:
        return {}

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token"
        )

    token = authorization.split(" ", 1)[1]
    if token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )

    return {}
