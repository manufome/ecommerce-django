# Serializer for the Shop model

from rest_framework import serializers
from apps.shop.models import Product, Category, Brand, ProductImage, Wishlist


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'parent', 'count', 'children')

    def get_children(self, obj):
        children = obj.get_children()
        return [CategorySerializer(children, many=True).data]
    
    def get_count(self, obj):
        subcategories = obj.get_descendants(include_self=True)
        return Product.objects.filter(category__in=subcategories).count()

    
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    large_pictures = ProductImageSerializer(many=True, read_only=True)
    category = CategorySerializer()
    brand = BrandSerializer()
    display_price = serializers.SerializerMethodField()
    pictures = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'
    
    def get_display_price(self, obj):
        return obj.get_display_price()
    
    def get_pictures(self, obj):
        return [{'url': obj.large_pictures.first().url, 'width': 150, 'height': 150}]
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['stock'] = str(representation['stock'])
        return representation

class HomeSerializer(serializers.Serializer):
    best_selling = ProductSerializer(many=True)
    featured = ProductSerializer(many=True)
    latest = ProductSerializer(many=True)
    on_sale = ProductSerializer(many=True)



# class WishlistSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#     products = ProductSerializer(many=True, read_only=True)
#     class Meta:
#         model = Wishlist
#         fields = '__all__'