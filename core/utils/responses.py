from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


def success_response(

    message="Success",
    data=None,
    status_code=HTTP_200_OK

):

    response_data = {

        "success": True,
        "message": message,
        "data": data,
        "errors": None
    }

    return Response(
        response_data,
        status=status_code
    )


def error_response(

    message="Something went wrong",
    errors=None,
    status_code=HTTP_400_BAD_REQUEST

):

    response_data = {

        "success": False,
        "message": message,
        "data": None,
        "errors": errors
    }

    return Response(
        response_data,
        status=status_code
    )