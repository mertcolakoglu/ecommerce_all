from rest_framework import permissions

class IsSupplierOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.profile.is_supplier

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class IsSupplierOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.profile.is_supplier and obj.supplier == request.user.profile

class IsSupplierOwnerOfProductOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.profile.is_supplier and obj.product.supplier == request.user.profile

class CanManageCart(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

class CanPlaceOrder(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.profile.is_supplier

class CanManageOwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CanReviewPurchasedProduct(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user and obj.product in [item.product for item in request.user.orders.all().values('items__product')]

class CanManageOwnNotifications(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    
class IsSupplierOwnerOfProductPricing(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.product.supplier == request.user.profile