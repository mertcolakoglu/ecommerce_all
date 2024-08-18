from rest_framework import serializers
from .models import Price, Discount, Promotion, PriceHistory

class PriceSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Price
        fields = ['id', 'product', 'base_price', 'currency', 'final_price', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['final_price'] = instance.get_final_price()
        return representation

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'product', 'name', 'percentage', 'start_date', 'end_date', 'is_active']

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'name', 'description', 'products', 'discount_type', 'discount_value', 'start_date', 'end_date', 'is_active']

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = ['id', 'product', 'price', 'date']