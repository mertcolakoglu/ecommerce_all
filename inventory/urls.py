from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, StockAdjustmentViewSet, ReorderPointViewSet

router = DefaultRouter()
router.register(r'inventory-items', InventoryItemViewSet)
router.register(r'stok-adjustments', StockAdjustmentViewSet)
router.register(r'reorder-points', ReorderPointViewSet)

urlpatterns = [
    path('', include(router.urls))
]
