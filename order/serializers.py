from django.http import HttpResponse
from rest_framework import serializers
from .models import cart,cartItem,Orders,Address,Payment


class CartSerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    def get_username(self,obj):
        return obj.user.username
    class Meta:
        model = cart
        fields= "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    product_name=serializers.SerializerMethodField()
    username=serializers.SerializerMethodField()
    def get_product_name(self,obj):
        return obj.product.name
    def get_username(self,obj):
        return obj.cart.user.username
    class Meta:
        model = cartItem
        fields = "__all__"

class OrderSerailizer(serializers.ModelSerializer):
    address=serializers.SerializerMethodField()
    def get_address(self,obj):
        return "{},{},{}".format(obj.cart.user.address.area,obj.cart.user.address.zone,obj.cart.user.address.mobile)
    
    class Meta:
        model=Orders
        fields="__all__"
    
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Payment
        fields="__all__"

