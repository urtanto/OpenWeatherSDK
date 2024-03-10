class APIError(Exception):
    """Основной класс исключения для ошибок API."""
    pass


class NotFoundError(APIError):
    """Исключение для случая, когда ресурс не найден (404)."""
    pass


class UnauthorizedError(APIError):
    """Исключение для ошибок аутентификации (401)."""
    pass


class InvalidCity(APIError):
    pass


class RequestError(APIError):
    """Исключение для остальных ошибок запроса."""
    pass