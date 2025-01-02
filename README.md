
# JWT Auth for FastAPI

This is a simple JWT authentication package for FastAPI that provides:

- JWT token creation
- Token verification and decoding
- Password hashing and verification
- FastAPI dependency injection for secure endpoints

## Installation

```bash
pip install jwt_auth
```

## Usage

### 1. Create a token:

```python
from jwt_auth.auth import create_access_token

# Create a JWT token
access_token = create_access_token({"sub": "username"}, secret_key, algorithm)
```

### 2. Use the dependency in FastAPI:

```python
from fastapi import FastAPI, Depends
from jwt_auth.dependencies import get_user_from_token

app = FastAPI()

@app.get("/users/me")
def read_users_me(current_user: str = Depends(get_user_from_token)):
    return {"user": current_user}
```