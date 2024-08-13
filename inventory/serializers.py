from rest_framework import serializers
from .models import InventoryItem, StockAdjustment, ReorderPoint

class InventoryItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'product_name', 'quantity', 'location']

class StockAdjustmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAdjustment
        fields = ['id', 'inventory_item', 'adjustment_type', 'quantity', 'reason', 'created_date']
    
class ReorderPointSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = ReorderPoint
        fields = ['id', 'product', 'product_name', 'min_quantity']