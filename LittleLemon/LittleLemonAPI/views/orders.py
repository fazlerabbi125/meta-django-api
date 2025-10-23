from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Order, OrderItem
from ..permissions import IsManager, IsCustomer, IsDeliveryCrew
from ..utils import CustomPageNumberPagination, GroupEnum
from rest_framework.throttling import ScopedRateThrottle

class OrderView(viewsets.GenericViewSet):
    lookup_url_kwarg="orderId"
    pagination_class = CustomPageNumberPagination
    throttle_scope = 'orders'
    
    def get_throttles(self):
        throttle_classes = []
        if self.action not in ('list', 'retrieve'):
            throttle_classes = [ScopedRateThrottle]
        return [throttle() for throttle in throttle_classes]