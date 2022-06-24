from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import cart,cartItem,Orders,Address,Payment,Payment_method,Delivery_method,Promocode
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer,UserShortSerializer
from main.serializers import ProductSerialaizer
from main.models import Product

class CartSerializer(serializers.ModelSerializer):
    user_details=serializers.SerializerMethodField()
    def get_user_details(self,obj):
        user_obj=User.objects.get(id=obj.user.id)
        nested_user_serializer=UserSerializer(user_obj)
        return nested_user_serializer.data
    class Meta:
        model = cart
        fields= "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    product_details=serializers.SerializerMethodField()
    def get_product_details(self,obj):
        product_obj=Product.objects.get(id=obj.product.id)
        nested_product_serializer=ProductSerialaizer(product_obj)
        return nested_product_serializer.data
    class Meta:
        model = cartItem
        fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    user_details=serializers.SerializerMethodField()
    def get_user_details(self,obj):
        user_obj=User.objects.get(id=obj.user.id)
        nested_user_serializer=UserShortSerializer(user_obj)
        return nested_user_serializer.data

    class Meta:
        model=Address
        fields="__all__"


class OrderSerailizer(serializers.ModelSerializer):
    address=serializers.SerializerMethodField()
    def get_address(self,obj):
        adrress_obj=Address.objects.get(id=obj.cart.user.user_have_address.id)
        nested_address_serializer=AddressSerializer(adrress_obj)
        return nested_address_serializer.data

    class Meta:
        model=Orders
        fields="__all__"
    

class PaymentSerializer(serializers.ModelSerializer):
    order=serializers.SerializerMethodField()
    def get_order(self,obj):
        order_obj=Orders.objects.get(id=obj.order.id)
        nested_order_serializer=OrderSerailizer(order_obj)
        return nested_order_serializer.data
    class Meta:
        model=Payment
        fields="__all__"

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model=Delivery_method
        fields="__all__"

class Pay_methodSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment_method
        fields="__all__"

class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Promocode
        fields="__all__"