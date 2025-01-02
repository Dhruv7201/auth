# jwt_auth/dependencies.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .auth import get_current_user, AuthError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        return get_current_user(token)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=e.detail)
