from rest_framework import viewsets, permissions, status, serializers
from rest_framework.response import Response
from ecommerce_all.permissions import IsSupplierOwnerOfProductOrReadOnly
from .models import InventoryItem, StockAdjustment, ReorderPoint
from .serializers import InventoryItemSerializer, StockAdjustmentSerializer, ReorderPointSerializer

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwnerOfProductOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product']
        location = serializer.validated_data['location']

        if product.supplier != self.request.user.profile:
            return Response({"detail": "You can only create inventory items for your own products."},
                            status=status.HTTP_403_FORBIDDEN)

        try:
            inventory_item = InventoryItem.objects.get(product=product, location=location)
            # If an existing item is found, update it
            inventory_item.quantity = serializer.validated_data['quantity']
            inventory_item.save()
            serializer = self.get_serializer(inventory_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except InventoryItem.DoesNotExist:
            # If no existing item is found, create a new one
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class StockAdjustmentViewSet(viewsets.ModelViewSet):
    queryset = StockAdjustment.objects.all()
    serializer_class = StockAdjustmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwnerOfProductOrReadOnly]

    def perform_create(self, serializer):
        adjustment = serializer.save()
        inventory_item = adjustment.inventory_item
        if adjustment.adjustment_type == 'increase':
            inventory_item.quantity += adjustment.quantity
        else:
            inventory_item.quantity -= adjustment.quantity
        inventory_item.save()

class ReorderPointViewSet(viewsets.ModelViewSet):
    queryset = ReorderPoint.objects.all()
    serializer_class = ReorderPointSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwnerOfProductOrReadOnly]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        if product.supplier == self.request.user.profile:
            serializer.save()
        else:
            raise serializers.ValidationError("You can only create reorder points for your own products.")