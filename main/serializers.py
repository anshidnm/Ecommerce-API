from rest_framework import serializers
from . models import Product,Category,Brand,Review,favourite
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer

class CategorySerialaizer(serializers.ModelSerializer):
    class Meta:
        model=Category
        exclude=('active',)


class BrandSerialaizer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        exclude=('active',)

class ProductSerialaizer(serializers.ModelSerializer):
    brand_details=serializers.SerializerMethodField()
    category_details=serializers.SerializerMethodField()

    def get_brand_details(self,obj):
        brand_obj=Brand.objects.get(id=obj.brand.id)
        nested_brand_serializer=BrandSerialaizer(brand_obj)
        return nested_brand_serializer.data

    def get_category_details(self,obj):
        category_obj=Category.objects.get(id=obj.category.id)
        nested_category_serializer=CategorySerialaizer(category_obj)
        return nested_category_serializer.data

    class Meta:
        model=Product
        exclude=('active',)



class ReviewSerialaizer(serializers.ModelSerializer):
    user_details=serializers.SerializerMethodField()
    product_details=serializers.SerializerMethodField()
    def get_user_details(self,obj):
        user_obj=User.objects.get(id=obj.user_reviewed.id)
        nested_user_serializer=UserSerializer(user_obj)
        return nested_user_serializer.data
    def get_product_details(self,obj):
        product_obj=Product.objects.get(id=obj.product_reviewed.id)
        nested_product_serializer=ProductSerialaizer(product_obj)
        return nested_product_serializer.data
    class Meta:
        model=Review
        fields="__all__"
        
class FavouriteSerializer(serializers.ModelSerializer):
    user_details=serializers.SerializerMethodField()
    product_details=serializers.SerializerMethodField()

    def get_user_details(self,obj):
        user_obj=User.objects.get(id=obj.user.id)
        nested_user_serializer=UserSerializer(user_obj)
        return nested_user_serializer.data
    
    def get_product_details(self,obj):
        product_obj=Product.objects.get(id=obj.product.id)
        nested_product_serializer=ProductSerialaizer(product_obj)
        return nested_product_serializer.data
    class Meta:
        model=favourite
        fields="__all__"
        
