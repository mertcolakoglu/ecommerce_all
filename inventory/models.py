from django.db import models
from products.models import Product

class InventoryItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventory')
    quantity = models.IntegerField(default=0)
    location = models.CharField(max_length=100)

    class Meta:
        unique_together = ['product', 'location']

    def __str__(self):
        return f"{self.product.name} - Qty: {self.quantity} at {self.location}"

class StockAdjustment(models.Model):
    ADJUSTMENT_TYPES = [
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
    ]
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='stock_adjustments')
    adjustment_type = models.CharField(max_length=20, choices=ADJUSTMENT_TYPES)
    quantity = models.IntegerField()
    reason = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adjustment_type} - {self.inventory_item.product.name} - Qty: {self.quantity}"

class ReorderPoint(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reorder_point')
    min_quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} - Min Qty: {self.min_quantity}"