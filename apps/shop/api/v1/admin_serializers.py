from rest_framework import serializers
from apps.shop.models import Product, Category, Brand

class AdminCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AdminBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class AdminProductSerializer(serializers.ModelSerializer):
    # Default PrimaryKeyRelatedField will be used for category and brand
    # which returns the ID instead of the object
    
    class Meta:
        model = Product
        fields = '__all__'
