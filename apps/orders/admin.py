from django.contrib import admin
from apps.orders.models import Address, Order, OrderItem, Payment, Coupon, Refund

admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(Refund)

# Register your models here.
