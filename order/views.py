from email.headerregistry import Address
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import CartSerializer,CartItemSerializer,OrderSerailizer,AddressSerializer,PaymentSerializer
from .models import cart,cartItem,Orders,Address,Payment
from rest_framework.response import Response


class cartViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=cart.objects.select_related('user').all()
    serializer_class=CartSerializer

    def list(self, request, *args, **kwargs):
        queryset=cart.objects.select_related('user').filter(user=request.user)
        if queryset.exists():
            serializer=CartSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'cart found'})
        else:
            return Response({'status':False,'data':None,'message':'cart not found'})

    def create(self, request, *args, **kwargs):
        data=request.data
        data['user']=request.user.id
        serializer=CartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'cart created'})
        else:
            return Response({'status':False,'data':None,'message':'cart not created'})
    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'cart deleted'})
        except:
            return Response({'status':False,'data':None,'message':'cart not deleted'})
           

class cartItemViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=cartItem.objects.select_related('product','cart').all()
    serializer_class=CartItemSerializer

    def list(self, request, *args, **kwargs):
        queryset=cartItem.objects.select_related('product','cart').filter(cart=request.user.cart)
        if queryset.exists():
            serializer=CartItemSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'CartItem found'})
        else:
            return Response({'status':False,'data':None,'message':'CartItem not found'})
    
    def create(self, request, *args, **kwargs):
        data=request.data
        data['cart']=request.user.cart.id
        serializer=CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'CartItem created'})
        else:
            return Response({'status':False,'data':None,'message':'CartItem not created'})

    def update(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            data=request.data
            data['cart']=request.user.cart.id
            serializer=CartItemSerializer(instance,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':'CartItem updated'})
            else:
                return Response({'status':False,'data':None,'message':'CartItem not updated'})
        except:
            return Response({'status':False,'data':None,'message':'CartItem not updated'})
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'CartItem deleted'})
        except:
            return Response({'status':False,'data':None,'message':'CartItem not deleted'})

           
            

class OrderViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Orders.objects.select_related('cart').all()
    serializer_class=OrderSerailizer

    def list(self, request, *args, **kwargs):
        queryset=Orders.objects.select_related('cart').filter(cart=request.user.cart)
        if queryset.exists():
            serializer=OrderSerailizer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Order found'})
        else:
            return Response({'status':False,'data':None,'message':'Order not found'})
            
    def create(self, request, *args, **kwargs):
        data=request.data
        data['cart']=request.user.cart.id
        serializer=OrderSerailizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'Order Created'})
        else:
            return Response({'status':False,'data':None,'message':'Order not Created'})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'Order Deleted'})            
        except:
            return Response({'status':False,'data':None,'message':'Order not Deleted'})

class AddressViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Address.objects.select_related('user').all()
    serializer_class=AddressSerializer

    def list(self, request, *args, **kwargs):
        queryset=Address.objects.select_related('user').filter(user=request.user)
        if queryset.exists():
            serializer=AddressSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Address Found'})
        else:
            return Response({'status':False,'data':None,'message':'Addrres not Found'})

    def create(self, request, *args, **kwargs):
        data=request.data
        data["user"]=request.user.id
        serializer=AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'Address Created'})
        else:
            return Response({'status':False,'data':None,'message':'Addrres not Created'})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'Addrres  Deleted'})
        except:
            return Response({'status':False,'data':None,'message':'Addrres not Deleted'})


        
class PaymentViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=PaymentSerializer
    queryset=Payment.objects.select_related('order','user').all()

    def list(self, request, *args, **kwargs):
        queryset=Payment.objects.select_related('order','user').filter(user=request.user)
        if queryset.exists():
            serializer=PaymentSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Payment Found'})
        else:
            return Response({'status':False,'data':None,'message':'Payment not Found'})

    def create(self, request, *args, **kwargs):
        data=request.data
        data['user']=request.user.id
        serializer=PaymentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'Payment Created'})
        else:
            return Response({'status':False,'data':None,'message':'Payment not Created'})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'Payment Deleted'})
        except:
            return Response({'status':False,'data':None,'message':'Payment not Deleted'})

