from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, scope: int = None, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.scope = scope

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme.")

            payload = self.verify_jwt(credentials.credentials)

            if not payload:
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token.")
            if self.scope and payload.get('scope') != self.scope:
                raise HTTPException(
                    status_code=403, detail="Permission Denied.")

            return payload
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decodeJWT(jwtoken)
            return payload
        except Exception:
            return None
