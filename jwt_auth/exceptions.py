# jwt_auth/exceptions.py


class AuthError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
