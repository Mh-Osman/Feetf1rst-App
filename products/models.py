from django.db import models

from decimal import Decimal

from  users.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 15.00 for 15%
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class Shoe(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unisex'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='shoes')
    subcategory = models.ForeignKey('SubCategory', on_delete=models.CASCADE, related_name='shoes', null=True, blank=True)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, related_name='shoes')
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    SKU = models.CharField(max_length=50, unique=True, null=True, blank=True)
    barcode = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='shoes/', null=True, blank=True)
    rating = models.FloatField(default=0.0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Discount fields
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))
    last_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.0'))

    def apply_discount(self, percentage):
        """Apply a discount based on a percentage value."""
        if percentage <= 0 or percentage > 100:
            self.discounted_price = self.price
            self.last_discount_percentage = Decimal('0.0')
        else:
            discount_amount = (self.price * Decimal(percentage)) / Decimal('100.0')
            self.discounted_price = self.price - discount_amount
            self.last_discount_percentage = Decimal(percentage)
            self.percentage = Decimal('0.0')

    def save(self, *args, **kwargs):
        # If a coupon is attached and active, use its discount
        if self.coupon and self.coupon.active:
            self.apply_discount(self.coupon.discount_percentage)
        # Otherwise, apply the manual percentage discount
        elif self.percentage > 0:
            self.apply_discount(self.percentage)
        else:
            self.discounted_price = self.price
            self.last_discount_percentage = Decimal('0.0')

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name