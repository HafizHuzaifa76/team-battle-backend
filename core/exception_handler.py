# core/exception_handler.py

import logging

from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import exception_handler
from rest_framework.response import Response

from core.utils.responses import error_response

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):

    # Handle DRF exceptions first
    response = exception_handler(exc, context)

    if response is not None:

        message = None

        if isinstance(response.data, dict):
            message = (
                response.data.get("detail")
                or response.data.get("message")
                or "Request failed"
            )
        else:
            message = str(response.data)

        return error_response(
            message = message,
            errors = response.data
        )

    # Handle unexpected exceptions
    logger.exception("Unhandled exception", exc_info=exc)

    return error_response(
        message = "Internal server error",
        status=HTTP_400_BAD_REQUEST
    )