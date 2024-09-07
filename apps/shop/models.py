from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
import math
from django.core.exceptions import ValidationError

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.URLField(max_length=1024, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_end_date = models.DateTimeField(null=True, blank=True)
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_new = models.BooleanField(default=False)
    is_top = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    ratings = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0.00), MaxValueValidator(5.00)])
    reviews_count = models.IntegerField(default=0)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def decrease_stock(self, quantity):
        if self.stock < quantity:
            raise ValidationError(f"Stock insuficiente para el producto {self.name}")
        self.stock -= quantity
        self.save()

    def get_display_price(self):
        if self.check_discount():
            discounted_price = self.price - (self.price * self.discount / 100)
            rounded_discounted_price = math.ceil(discounted_price / 50) * 50
            return [rounded_discounted_price, self.price]
        return [self.price, self.price]

    def check_discount(self):
        if self.discount > 0 and self.discount_end_date:
            return self.discount_end_date > timezone.now()
        return False
    
    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='large_pictures')
    url = models.URLField(max_length=1024)
    width = models.IntegerField(default=600)
    height = models.IntegerField(default=600)

    def __str__(self):
        return f"{self.product.name} Image"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.user.username}"
