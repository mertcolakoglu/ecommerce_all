from django.urls import path, include
from .views import ProductListCreateView, CategoryListCreateView, ProductTagListCreateView, ProductTagDetailUpdateDeleteView, ProductImageDetailUpdateDeleteView, ProductDetailUpdateDeleteView,ProductImageListCreateView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailUpdateDeleteView.as_view(), name = 'product-detail-update-delete'),
    path('product-images/', ProductImageListCreateView.as_view(), name='productimage-list-create'),
    path('product-images/<int:pk>/', ProductImageDetailUpdateDeleteView.as_view(), name='productimage-detail-update-delete'),
    path('product-tags/', ProductTagListCreateView.as_view(), name='producttag-list-create'),
    path('product-tags/<int:pk>/', ProductTagDetailUpdateDeleteView.as_view(), name='producttag-detail-update-delete'),
]