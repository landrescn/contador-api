# auth.py
import os, time
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
JWT_SECRET = os.getenv("JWT_SECRET", "change")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
security = HTTPBearer()
def create_token(sub: str, role: str = "viewer", exp_sec: int = 3600):
payload = {"sub": sub, "role": role, "exp": int(time.time()) + exp_sec}
return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)
def require_token(creds: HTTPAuthorizationCredentials = Depends(security)):
try:
payload = jwt.decode(creds.credentials, JWT_SECRET,
algorithms=[JWT_ALG])
return payload
except JWTError:
raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
detail="Invalid token")