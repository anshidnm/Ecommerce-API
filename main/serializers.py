from dataclasses import fields
from pydoc import classname
from pyexpat import model
from rest_framework import serializers
from . models import Product,Category,Brand,Review,favourite


class ProductSerialaizer(serializers.ModelSerializer):
    brand_name=serializers.SerializerMethodField()
    category_name=serializers.SerializerMethodField()
    def get_brand_name(self,obj):
        return obj.brand.brand_name
    def get_category_name(self,obj):
        return obj.category.category_name
    class Meta:
        model=Product
        exclude=('active',)

class CategorySerialaizer(serializers.ModelSerializer):
    class Meta:
        model=Category
        exclude=('active',)

class BrandSerialaizer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        exclude=('active',)

class ReviewSerialaizer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    product=serializers.SerializerMethodField()
    def get_username(self,obj):
        return obj.user_reviewed.username
    def get_product(self,obj):
        return obj.product_reviewed.name
    class Meta:
        model=Review
        fields="__all__"
        
class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=favourite
        fields="__all__"
        
