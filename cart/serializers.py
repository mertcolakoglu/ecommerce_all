from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only = True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only = True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price', 'added_at']
    
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True, read_only = True)
    total_cart_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_cart_price', 'created_at', 'updated_at']

    def get_total_price(self, obj):
        return sum(item.total_price for item in obj.items.all())