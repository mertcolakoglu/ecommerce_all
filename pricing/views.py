from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Price, Discount, Promotion, PriceHistory
from .serializers import PriceSerializer, DiscountSerializer, PromotionSerializer, PriceHistorySerializer
from ecommerce_all.permissions import IsSupplierOwnerOfProductPricing
from products.models import Product

class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwnerOfProductPricing]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        if product.supplier == self.request.user.profile:
            price = serializer.save()
            PriceHistory.objects.create(product=product, price=price.base_price)
        else:
            raise serializers.ValidationError("You can only set prices for your own products.")

    def perform_update(self, serializer):
        old_price = self.get_object()
        new_price = serializer.save()
        if old_price.base_price != new_price.base_price:
            PriceHistory.objects.create(product=new_price.product, price=new_price.base_price)

    @action(detail=True, methods=['get'])
    def price_history(self, request, pk=None):
        price = self.get_object()
        history = PriceHistory.objects.filter(product=price.product).order_by('-date')
        serializer = PriceHistorySerializer(history, many=True)
        return Response(serializer.data)

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwnerOfProductPricing]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        if product.supplier == self.request.user.profile:
            serializer.save()
        else:
            raise serializers.ValidationError("You can only create discounts for your own products.")

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplierOwnerOfProductPricing]

    def perform_create(self, serializer):
        products = serializer.validated_data['products']
        if all(product.supplier == self.request.user.profile for product in products):
            serializer.save()
        else:
            raise serializers.ValidationError("You can only create promotions for your own products.")

    @action(detail=True, methods=['post'])
    def apply_to_products(self, request, pk=None):
        promotion = self.get_object()
        product_ids = request.data.get('product_ids', [])
        products = Product.objects.filter(id__in=product_ids, supplier=request.user.profile)
        
        if not products:
            return Response({"detail": "No valid products found."}, status=status.HTTP_400_BAD_REQUEST)
        
        promotion.products.add(*products)
        return Response({"detail": f"Promotion applied to {products.count()} products."}, status=status.HTTP_200_OK)