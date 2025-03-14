from rest_framework import status
from rest_framework.exceptions import APIException


class KwargIntException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Pls input a correct pk ej: 1, 2, 3"
    default_code = "invalid_kwarg"
