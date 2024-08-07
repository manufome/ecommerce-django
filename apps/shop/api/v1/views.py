# Views for the shop app
# https://www.django-rest-framework.org/api-guide/filtering/  reference for filtering ✏


from apps.shop.api.v1.serializers import ProductSerializer, CategorySerializer, BrandSerializer, WishlistSerializer
from apps.shop.models import Product, Category, Brand, Wishlist
from rest_framework import viewsets
from .filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filterset_class = ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(parent=None)
    serializer_class = CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.kwargs['user_id'])




