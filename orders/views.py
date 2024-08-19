from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer
from ecommerce_all.permissions import CanPlaceOrder

# Create your views here.

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.profile.is_supplier:
            return Order.objects.filter(items__product__supplier = user.profile)
        return Order.objects.filter(user = user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        return OrderSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [CanPlaceOrder()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return Response({'status': 'Order cancelled'})
        return Response({'error': 'Cannot cancel this order'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_status (self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        if self.request.user.profile.is_supplier:
            allowed_updates = {
                'pending': 'processing',
                'processing': 'shipped',
            }
            if order.status in allowed_updates and new_status == allowed_updates[order.status]:
                order.status = new_status
                order.save()
                return Response ({'status': 'Order status updated'})
            return Response({'error': 'You are not allowed to perform this status update'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({'error': 'You are not allowed to update order status'}, status=status.HTTP_403_FORBIDDEN)