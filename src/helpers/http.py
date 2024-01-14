import httpx

from exceptions import (
    BadRequestError,
    UnauthorizedError,
    PermissionDeniedError,
    NotFoundError,
    StocksUpdateError,
    TooManyRequestsError,
    WildberriesAPIError,
)

__all__ = ('handle_error_status_code',)


def handle_error_status_code(response: httpx.Response) -> None:
    if not response.is_error:
        return
    status_code_to_exception_class = {
        400: BadRequestError,
        401: UnauthorizedError,
        403: PermissionDeniedError,
        404: NotFoundError,
        409: StocksUpdateError,
        429: TooManyRequestsError,
    }
    exception_class: type[WildberriesAPIError] = (
        status_code_to_exception_class.get(
            response.status_code,
            WildberriesAPIError,
        )
    )
    raise exception_class(response)
