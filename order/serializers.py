from rest_framework import serializers
from .models import cart,cartItem,Orders,Address,Payment
from django.contrib.auth.models import User
from accounts.serializers import UserSerializer 
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
    cart_details=serializers.SerializerMethodField()
    def get_product_details(self,obj):
        product_obj=Product.objects.get(id=obj.product.id)
        nested_product_serializer=ProductSerialaizer(product_obj)
        return nested_product_serializer.data
    def get_cart_details(self,obj):
        cart_obj=cart.objects.get(id=obj.cart.id)
        nested_cart_serializer=CartSerializer(cart_obj)
        return nested_cart_serializer.data
    class Meta:
        model = cartItem
        fields = "__all__"

class AddressSerializer(serializers.ModelSerializer):
    user_details=serializers.SerializerMethodField()
    def get_user_details(self,obj):
        user_obj=User.objects.get(id=obj.user.id)
        nested_user_serializer=UserSerializer(user_obj)
        return nested_user_serializer.data

    class Meta:
        model=Address
        fields="__all__"


class OrderSerailizer(serializers.ModelSerializer):
    address=serializers.SerializerMethodField()
    cart_details=serializers.SerializerMethodField()
    def get_cart_details(self,obj):
        cart_obj=cart.objects.get(id=obj.cart.id)
        nested_cart_serializer=CartSerializer(cart_obj)
        return nested_cart_serializer.data

    def get_address(self,obj):
        adrress_obj=Address.objects.get(id=obj.cart.user.user_have_address.id)
        nested_address_serializer=AddressSerializer(adrress_obj)
        return nested_address_serializer.data

    class Meta:
        model=Orders
        fields="__all__"
    

class PaymentSerializer(serializers.ModelSerializer):
    user_details=serializers.SerializerMethodField()
    order_details=serializers.SerializerMethodField()
    def get_user_details(self,obj):
        user_obj=User.objects.get(id=obj.user.id)
        nested_user_serializer=UserSerializer(user_obj)
        return nested_user_serializer.data
    def get_order_details(self,obj):
        order_obj=Orders.objects.get(id=obj.order.id)
        nested_order_serializer=OrderSerailizer(order_obj)
        return nested_order_serializer.data
    class Meta:
        model=Payment
        fields="__all__"

