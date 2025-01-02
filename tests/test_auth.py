# tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from jwt_auth.auth import create_access_token
from jwt_auth.dependencies import get_user_from_token
from fastapi import FastAPI, Depends, HTTPException

# Create FastAPI app instance
app = FastAPI()

# Dependency for testing
@app.get("/users/me")
def read_users_me(current_user: str = Depends(get_user_from_token)):
    return {"user": current_user}

# Test client
client = TestClient(app)


@pytest.fixture
def valid_token():
    return create_access_token({"sub": "testuser"})


def test_read_users_me(valid_token):
    response = client.get("/users/me", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.json() == {"user": "testuser"}


def test_invalid_token():
    response = client.get("/users/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}
