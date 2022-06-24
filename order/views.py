from email.headerregistry import Address
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny

from constantVariables import *
from .serializers import CartSerializer,CartItemSerializer,OrderSerailizer,AddressSerializer, Pay_methodSerializer,PaymentSerializer,DeliverySerializer,Payment_method,PromoSerializer
from .models import cart,cartItem,Orders,Address,Payment,Delivery_method,Payment_method,Promocode
from rest_framework.response import Response


class cartViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=cart.objects.all()
    serializer_class=CartSerializer

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('user').filter(user=request.user)
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':CART_FOUND})
        else:
            return Response({'status':False,'data':None,'message':CART_NOT_FOUND})

    def create(self, request, *args, **kwargs):
        data=request.data
        data['user']=request.user.id
        serializer=self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':CART_CREATED})
        else:
            return Response({'status':False,'data':None,'message':CART_NOT_CREATED})
    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':CART_DELETED})
        except:
            return Response({'status':False,'data':None,'message':CART_NOT_DELETED})
           

class cartItemViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=cartItem.objects.all()
    serializer_class=CartItemSerializer

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('product','cart').filter(cart=request.user.cart)
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':CART_ITEM_FOUND})
        else:
            return Response({'status':False,'data':None,'message':CART_ITEM_NOT_FOUND})
    
    def create(self, request, *args, **kwargs):
        data=request.data
        data['cart']=request.user.cart.id
        serializer=self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':CART_ITEM_CREATED})
        else:
            return Response({'status':False,'data':None,'message':CART_ITEM_NOT_CREATED})

    def update(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            data=request.data
            data['cart']=request.user.cart.id
            serializer=self.get_serializer(instance,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':CART_ITEM_UPDATED})
            else:
                return Response({'status':False,'data':None,'message':CART_ITEM_NOT_UPDATED})
        except:
            return Response({'status':False,'data':None,'message':CART_ITEM_NOT_UPDATED})
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':CART_ITEM_DELETED})
        except:
            return Response({'status':False,'data':None,'message':CART_ITEM_NOT_DELETED})

           
            

class OrderViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Orders.objects.all()
    serializer_class=OrderSerailizer

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('cart').filter(cart=request.user.cart)
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':ORDER_FOUND})
        else:
            return Response({'status':False,'data':None,'message':ORDER_NOT_FOUND})
            
    def create(self, request, *args, **kwargs):
        data=request.data
        data['cart']=request.user.cart.id
        data['address'].request.user.address.id
        serializer=self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':ORDER_CREATED})
        else:
            return Response({'status':False,'data':None,'message':ORDER_NOT_CREATED})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':ORDER_DELETED})            
        except:
            return Response({'status':False,'data':None,'message':ORDER_NOT_DELETED})

class AddressViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Address.objects.all()
    serializer_class=AddressSerializer

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('user').filter(user=request.user)
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':ADDRESS_FOUND})
        else:
            return Response({'status':False,'data':None,'message':ADDRESS_NOT_FOUND})

    def create(self, request, *args, **kwargs):
        data=request.data
        data["user"]=request.user.id
        serializer=self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':ADDRESS_CREATED})
        else:
            return Response({'status':False,'data':None,'message':ADDRESS_NOT_CREATED})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':ADDRESS_DELETED})
        except:
            return Response({'status':False,'data':None,'message':ADDRESS_NOT_DELETED})


        
class PaymentViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=PaymentSerializer
    queryset=Payment.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('order','user').filter(user=request.user)
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':PAYMENT_FOUND})
        else:
            return Response({'status':False,'data':None,'message':PAYMENT_NOT_FOUND})

    def create(self, request, *args, **kwargs):
        data=request.data
        data['user']=request.user.id
        serializer=self.get_serializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':PAYMENT_ADDED})
            else:
                return Response({'status':False,'data':None,'message':PAYMENT_NOT_ADDED})
        except:
            return Response({'status':False,'data':None,'message':PAYMENT_NOT_ADDED})


    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':PAYMENT_DELETED})
        except:
            return Response({'status':False,'data':None,'message':PAYMENT_NOT_DELETED})

class DeliveryViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=DeliverySerializer
    queryset=Delivery_method.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':DELIVERY_FOUND})
        else:
            return Response({'status':False,'data':None,'message':DELIVERY_NOT_FOUND})

class PromoViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=PromoSerializer
    queryset=Promocode.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':PROMO_FOUND})
        else:
            return Response({'status':False,'data':None,'message':PROMO_NOT_FOUND})

class PaymethodViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=Pay_methodSerializer
    queryset=Payment_method.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':PAY_METHOD_FOUND})
        else:
            return Response({'status':False,'data':None,'message':PAY_METHOD_NOT_FOUND})
