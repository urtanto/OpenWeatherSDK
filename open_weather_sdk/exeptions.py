class APIError(Exception):
    """Base exception class for the API exceptions."""
    pass


class NotFoundError(APIError):
    """Exception raised when a requested resource is not found (404)."""
    pass


class UnauthorizedError(APIError):
    """Exception raised for authentication errors (401)."""
    pass


class InvalidCity(APIError):
    """Exception raised when the specified city is invalid or not recognized by the API."""
    pass


class RequestError(APIError):
    """Исключение для остальных ошибок запроса."""
    pass