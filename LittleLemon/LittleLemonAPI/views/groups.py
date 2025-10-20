from rest_framework.response import Response
from enum import StrEnum

class GroupEnum(StrEnum):
    DELIVERY_CREW = "Delivery crew"
    MANAGER = "Manager"
    # Users not assigned to a group will be considered customers