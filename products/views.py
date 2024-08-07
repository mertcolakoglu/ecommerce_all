from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Category, Product, ProductImage, ProductTag
from .serializers import CategorySerializer, ProductCreateUpdateSerializer, ProductImageSerializer, ProductSerializer, ProductTagSerializer
from ecommerce_all.permissions import IsSupplierOrReadOnly, IsSupplierOwnerOrReadOnly

# Create your views here.

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSupplierOrReadOnly()]

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSupplierOrReadOnly()]

    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user.profile)

class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSupplierOwnerOrReadOnly()]

class ProductImageListCreateView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSupplierOrReadOnly()]

class ProductImageDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSupplierOrReadOnly()]

class ProductTagListCreateView(generics.ListCreateAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSupplierOrReadOnly()]

class ProductTagDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated(), IsSupplierOrReadOnly()]