# shop app urls.py
from django.urls import path, include
from apps.shop.api.v1.views import ProductViewSet, CategoryViewSet, BrandViewSet, HomeListView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('brands', BrandViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('home/', HomeListView.as_view(), name='home'),
]
