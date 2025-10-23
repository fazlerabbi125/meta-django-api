from enum import StrEnum
from rest_framework.request import Request, HttpRequest
from rest_framework import status, exceptions, pagination

type DrfRequest = Request | HttpRequest


class GroupEnum(StrEnum):
    DELIVERY_CREW = "Delivery crew"
    MANAGER = "Manager"
    # Users not assigned to a group will be considered customers


class ConflictFound(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict found with the current state of the target resource"
    default_code = "conflict_found"

class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "limit"
    max_page_size = 100