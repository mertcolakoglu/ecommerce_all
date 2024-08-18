from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PriceViewSet, DiscountViewSet, PromotionViewSet

router = DefaultRouter()
router.register(r'prices', PriceViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'promotions', PromotionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]