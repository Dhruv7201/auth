# jwt_auth/auth.py

import jwt
import datetime
from passlib.context import CryptContext
from typing import Optional
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException

# Secret key for encoding and decoding JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT exception handling
class AuthError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Function to hash a password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Function to decode the JWT and get the payload
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise AuthError("Token has expired")
    except InvalidTokenError:
        raise AuthError("Invalid token")


# Function to get the current user from the token
def get_current_user(token: str):
    try:
        payload = decode_access_token(token)
        return payload.get("sub")
    except AuthError as e:
        raise e
