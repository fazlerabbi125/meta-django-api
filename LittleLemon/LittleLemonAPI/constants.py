from enum import StrEnum
from rest_framework.request import Request, HttpRequest

class GroupEnum(StrEnum):
    DELIVERY_CREW = "Delivery crew"
    MANAGER = "Manager"
    # Users not assigned to a group will be considered customers

type DrfRequest = Request | HttpRequest