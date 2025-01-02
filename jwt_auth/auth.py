# jwt_auth/auth.py

import jwt
import datetime
from passlib.context import CryptContext
from typing import Optional
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException
import os
import secrets


ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Auth:
    def __init__(self, secret_key: str, algorithm: str):
        self.secret_key = secret_key
        self.algorithm = algorithm

    # setter for secret key
    def set_secret_key(self, secret_key: str):
        self.secret_key = secret_key

    # setter for algorithm
    def set_algorithm(self, algorithm: str):
        self.algorithm = algorithm

    # getter for secret key
    def get_secret_key(self):
        return self.secret_key
    
    # getter for algorithm
    def get_algorithm(self):
        return self.algorithm
    
auth = Auth(secret_key=None, algorithm=None)

# JWT exception handling
class AuthError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)


# Function to create access token
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM) -> str:
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Secret key for encoding and decoding JWT
    if not secret_key:
        SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    else:
        SECRET_KEY = secret_key
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY not found")
    if not algorithm:
        ALGORITHM = "HS256"
    else:
        ALGORITHM = algorithm
    if not ALGORITHM:
        raise ValueError("ALGORITHM not found")
    
    auth.set_secret_key(SECRET_KEY)
    auth.set_algorithm(ALGORITHM)
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
        SECRET_KEY = auth.get_secret_key()
        ALGORITHM = auth.get_algorithm()
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY not found in Auth object")
        if not ALGORITHM:
            raise ValueError("ALGORITHM not found in Auth object")
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
