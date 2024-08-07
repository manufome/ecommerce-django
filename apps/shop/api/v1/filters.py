# import django_filters
from apps.shop.models import Product, Category
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.db.models import F, ExpressionWrapper, DecimalField

class ProductFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug', method='filter_by_category')
    brands = filters.CharFilter(field_name='brand__slug', method='filter_by_brands')
    min_price = filters.NumberFilter(field_name="price", method='filter_by_min_price')
    max_price = filters.NumberFilter(field_name="price", method='filter_by_max_price')

    class Meta:
        model = Product
        fields = ['is_new', 'is_top', 'is_featured']

    def filter_by_category(self, queryset, name, value):
        category = get_object_or_404(Category, slug=value)
        subcategories = category.get_descendants(include_self=True)
        return queryset.filter(category__in=subcategories)
    
    def filter_by_brands(self, queryset, name, value):
        brands = value.split(',')
        return queryset.filter(brand__slug__in=brands)
    
    def filter_by_min_price(self, queryset, name, value):
        queryset = queryset.annotate(
            discount_price=ExpressionWrapper(
                F('price') - (F('price') * F('discount') / 100),
                output_field=DecimalField()
            )
        )
        return queryset.filter(discount_price__gte=value)
    
    def filter_by_max_price(self, queryset, name, value):
        queryset = queryset.annotate(
            discount_price=ExpressionWrapper(
                F('price') - (F('price') * F('discount') / 100),
                output_field=DecimalField()
            )
        )
        return queryset.filter(discount_price__lte=value)