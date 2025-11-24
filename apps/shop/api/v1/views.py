# Views for the shop app
# https://www.django-rest-framework.org/api-guide/filtering/  reference for filtering ✏

from apps.shop.api.v1.serializers import ProductSerializer, CategorySerializer, BrandSerializer, HomeSerializer
from apps.shop.api.v1.admin_serializers import AdminProductSerializer, AdminCategorySerializer, AdminBrandSerializer
from apps.shop.models import Product, Category, Brand, Wishlist
from rest_framework import viewsets, generics  
from .filters import ProductFilter
from rest_framework.response import Response

class HomeListView(generics.GenericAPIView):
    serializer_class = HomeSerializer

    def get(self, request, *args, **kwargs):
        limit = int(request.query_params.get('limit', 5))
        best_selling = Product.objects.filter(is_top=True).order_by('-discount')[:limit] # luego cambiar por los productos mas vendidos en una semana
        featured = Product.objects.filter(is_featured=True).order_by('-discount')[:limit]
        latest = Product.objects.order_by('-created_at')[:limit]
        on_sale = Product.objects.filter(discount__gt=0).order_by('-discount')[:limit]

        data = {
            'best_selling': best_selling,
            'featured': featured,
            'latest': latest,
            'on_sale': on_sale
        }

        serializer = self.get_serializer(data)
        return Response(serializer.data)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']

    def get_serializer_class(self):
        if self.request.query_params.get('flat') == 'true':
            return AdminProductSerializer
        return ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # If flat is requested, return standard retrieve response (no wrapping)
        if self.request.query_params.get('flat') == 'true':
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        previous = Product.objects.filter(id__lt=instance.id).order_by('-id').first()
        next = Product.objects.filter(id__gt=instance.id).order_by('id').first()
        related = Product.objects.filter(category=instance.category).exclude(id=instance.id).order_by('?')[:4]

        serializer = self.get_serializer(instance)
        previous_serializer = self.get_serializer(previous) if previous else None
        next_serializer = self.get_serializer(next) if next else None
        related_serializer = self.get_serializer(related, many=True)
        
        return Response({
            'product': serializer.data,
            'previous': previous_serializer.data if previous_serializer else None,
            'next': next_serializer.data if next_serializer else None,
            'related': related_serializer.data if related_serializer else None
        })

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_serializer_class(self):
        if self.request.query_params.get('flat') == 'true':
            return AdminCategorySerializer
        return CategorySerializer

    def get_queryset(self):
        if self.action == 'list':
            if self.request.query_params.get('show_all') == 'true':
                return Category.objects.all()
            return Category.objects.filter(parent=None)
        return Category.objects.all()

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_serializer_class(self):
        if self.request.query_params.get('flat') == 'true':
            return AdminBrandSerializer
        return BrandSerializer

# class WishlistViewSet(viewsets.ModelViewSet):
#     queryset = Wishlist.objects.all()
#     serializer_class = WishlistSerializer

#     def get_queryset(self):
#         return Wishlist.objects.filter(user=self.kwargs['user_id'])




