from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChoicesView, AddressViewSet, OrderViewSet, OrderItemViewSet, PaymentViewSet, CouponViewSet, RefundViewSet

router = DefaultRouter()
router.register(r'addresses', AddressViewSet, basename='addresses')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order-items', OrderItemViewSet, basename='order-items')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'coupons', CouponViewSet, basename='coupons')
router.register(r'refunds', RefundViewSet, basename='refunds')

urlpatterns = [
    path('', include(router.urls)),
    path('choices/', ChoicesView.as_view(), name='choices'),
]