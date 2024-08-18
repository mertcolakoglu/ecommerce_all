from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import CartSerializer
from products.models import Product

# Create your views here.

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)
    
    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id = product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart = cart, product = product)

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()
        
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def reomve_from_cart(self, request):
        product_id = request.data.get('product_id')

        try:
            cart = Cart.objects.get(user = self.request.user)
            cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
            cart_item.delete()
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action (detail=False, methods=['post'])
    def update_quantity(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)

        try:
            cart = Cart.objects.get(user = request.user)
            cart_item = CartItem.objects.get(cart = cart, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
        except (Cart.DoesNotExist, CartItem.DoesNotExist):
            return Response({'error': 'Item not found in cart'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    @action (detail=False, methods=['post'])
    def clear_cart(self, request):
        try:
            cart = Cart.objects.get(user = request.user)
            cart.items.all().delete()
        except Cart.DoesNotExist:
            pass
    
        return Response({'message': 'Cart cleared succesfully'})