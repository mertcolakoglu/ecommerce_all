from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Category, Product, ProductImage, ProductTag
from .serializers import CategorySerializer, ProductCreateUpdateSerializer, ProductImageSerializer, ProductSerializer, ProductTagSerializer
from ecommerce_all.permissions import IsSupplierOrReadOnly

# Create your views here.

class CategoryListCreateView (mixins.ListModelMixin,
                              mixins.CreateModelMixin,
                              generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsSupplierOrReadOnly()]
    
    def get (self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post (self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductListCreateView (mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             generics.GenericAPIView):
    
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsSupplierOrReadOnly()]
    
    def get (self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post (self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsSupplierOrReadOnly()]

class ProductImageListCreateView(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 generics.GenericAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsSupplierOrReadOnly()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ProductImageDetailUpdateDeleteView (generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsSupplierOrReadOnly()]

class ProductTagListCreateView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsSupplierOrReadOnly()]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ProductTagDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductTag.objects.all()
    serializer_class = ProductTagSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsSupplierOrReadOnly()]