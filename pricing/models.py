from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product

class Price(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='price')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.base_price} {self.currency}"

    def get_final_price(self):
        discounts = self.product.discounts.filter(is_active=True)
        promotions = self.product.promotions.filter(is_active=True)
        
        final_price = self.base_price

        for discount in discounts:
            final_price *= (1 - discount.percentage / 100)

        for promotion in promotions:
            if promotion.discount_type == 'percentage':
                final_price *= (1 - promotion.discount_value / 100)
            elif promotion.discount_type == 'fixed':
                final_price -= promotion.discount_value

        return max(final_price, 0)

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='discounts')
    name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)])
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.name} ({self.percentage}% off)"

class Promotion(models.Model):
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    products = models.ManyToManyField(Product, related_name='promotions')
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.discount_value}{' %' if self.discount_type == 'percentage' else ''} off"

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.price} at {self.date}"