from fastapi import HTTPException

class TokenNotFoundException(HTTPException):
    def __init__(self, status_code: int = 401, message: str = "Token not found"):
        super().__init__(status_code, message)

class TokenExpiredException(HTTPException):
    def __init__(self, status_code: int = 401, message: str = "Token has expired"):
        super().__init__(status_code, message)