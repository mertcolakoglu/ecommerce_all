from rest_framework import serializers
from .models import Review
from django.contrib.auth.models import AnonymousUser

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    product = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment']
    
    def validate(self, data):
        user = self.context['request'].user

        if isinstance(user, AnonymousUser):
            raise serializers.ValidationError("You must be logged in to write a review.")

        product = data['product']

        if not user.orders.filter(items__product=product).exists():
            raise serializers.ValidationError("You can only review products you have purchased.")

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Review.objects.create(user = user, **validated_data)