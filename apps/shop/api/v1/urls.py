# shop app urls.py
from django.urls import path, include
from apps.shop.api.v1.views import ProductViewSet, CategoryViewSet, BrandViewSet, WishlistViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('brands', BrandViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
