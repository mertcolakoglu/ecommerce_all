from rest_framework import serializers
from .models import Order, OrderItem, ShippingAddress
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'country', 'zip_code']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'total_price', 'items', 'shipping_address']
        read_only_fields = ['user', 'created_at', 'updated_at']

class CreateOrderSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = Order
        fields = ['shipping_address']

    def create(self, validated_data):
        shipping_address_data = validated_data.pop('shipping_address')
        user = self.context['request'].user
        cart = user.cart

        if not cart.items.exists():
            raise serializers.ValidationError("Cannot create an order with an empty cart.")

        total_price = sum(item.product.price.get_final_price() * item.quantity for item in cart.items.all())
        
        order = Order.objects.create(user=user, total_price=total_price, **validated_data)
        ShippingAddress.objects.create(order=order, **shipping_address_data)

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price.get_final_price()
            )

        cart.items.all().delete()

        return order