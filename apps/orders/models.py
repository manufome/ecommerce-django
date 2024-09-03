from django.db import models
from apps.shop.models import Product
from django.contrib.auth.models import User
from .choices import LOCALITIES, STREET_TYPES, ORDER_STATUS, PAYMENT_METHODS

# https://django-payments.readthedocs.io/en/stable/usage.html
# https://www.mercadopago.com.co/developers/es/docs/checkout-api/integration-configuration/pse#editor_6


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locality = models.CharField(max_length=3, choices=LOCALITIES)
    street_type = models.CharField(max_length=3, choices=STREET_TYPES)
    street_value = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    complement = models.CharField(max_length=255)
    address_type = models.CharField(max_length=10, choices=(('B', 'Billing'), ('S', 'Shipping')))
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=ORDER_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.SET_NULL, null=True)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, null=True)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20)

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)