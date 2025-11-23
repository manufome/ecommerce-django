from django.db import models
from apps.shop.models import Product
from django.contrib.auth.models import User
from .choices import Locality, StreetType, PaymentMethod, OrderStatus, PaymentStatus

# https://django-payments.readthedocs.io/en/stable/usage.html
# https://www.mercadopago.com.co/developers/es/docs/checkout-api/integration-configuration/pse#editor_6


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    locality = models.CharField(max_length=3, choices=Locality.choices)
    street_type = models.CharField(max_length=3, choices=StreetType.choices)
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
    status = models.CharField(max_length=1, choices=OrderStatus.choices)
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

    @property
    def subtotal(self):
        return self.quantity * self.price

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=3, choices=PaymentMethod.choices)
    status = models.CharField(max_length=1, choices=PaymentStatus.choices)

    def calculate_shipping_cost(self):
        if self.amount > 50000 or self.payment_method==PaymentMethod.IN_STORE:
            return 0
        return 7000
    
    def save(self, *args, **kwargs):
        self.shipping_cost = self.calculate_shipping_cost()
        self.amount += self.shipping_cost
        super().save(*args, **kwargs)

class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)