__all__ = (
    'BaseError', 'RequestError', 'ForbiddenRequestError', 'UnknownRequestError'
)


class BaseError(Exception):
    """Base class for exceptions in Yandex.Weather API."""

    def __init__(self, message=None):
        if message is None:
            message = self.__class__.__doc__

        self.message = message
        super().__init__(message)


class RequestError(BaseError):
    """Not successful request to API."""


class ForbiddenRequestError(RequestError):
    """Request to API resulted in 403 status."""


class UnknownRequestError(RequestError):
    """Bizarre error while requesting API."""
