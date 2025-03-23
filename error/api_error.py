from fastapi import HTTPException


class APIError(HTTPException):
    """Base class for API-related errors."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(status_code,f"API Error : {message}")


class BadRequestError(APIError):
    """400 Bad Request"""

    def __init__(self, message="Bad Request"):
        super().__init__(400,f"API Error : {message}")


class UnauthorizedError(APIError):
    """401 Unauthorized"""

    def __init__(self, message="Unauthorized Access"):
        super().__init__(401,f"API Error : {message}")


class ServerError(APIError):
    """500 Internal Server Error"""

    def __init__(self, message="Internal Server Error"):
        super().__init__(500,f"API Error : {message}")