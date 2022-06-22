from . models import Review,Category,Brand,Product,favourite
from . serializers import ProductSerialaizer,CategorySerialaizer,BrandSerialaizer,ReviewSerialaizer,FavouriteSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q
from django.db.models import Prefetch
from rest_framework.response import Response

class CategoryViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Category.objects.filter(active=True)
    serializer_class=CategorySerialaizer

    def list(self, request, *args, **kwargs):
        queryset=Category.objects.filter(active=True)
        if queryset.exists():
            serializer=CategorySerialaizer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Category found'})
        else:
            return Response({'status':False,'data':None,'message':'Category not found'})


class BrandViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Brand.objects.filter(active=True)
    serializer_class=BrandSerialaizer

    def list(self, request, *args, **kwargs):
        queryset=Brand.objects.filter(active=True)
        if queryset.exists():
            serializer=BrandSerialaizer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Brands found'})
        else:
            return Response({'status':False,'data':None,'message':'Brands not found'})
    

class ProductViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Product.objects.select_related('category').filter( Q(active=True) & Q(stock__gt=0) )
    serializer_class=ProductSerialaizer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['category','brand']

    def list(self, request, *args, **kwargs):
        queryset=Product.objects.select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) )
        if queryset.exists():
            serializer=ProductSerialaizer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Products found'})
        else:
            return Response({'status':False,'data':None,'message':'Products not found'})
          


class ReviewViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Review.objects.select_related('user_reviewed','product_reviewed').all()
    serializer_class=ReviewSerialaizer
    
    def list(self, request, *args, **kwargs):
        queryset=Review.objects.select_related('user_reviewed','product_reviewed').all()
        if queryset.exists():
            serializer=ReviewSerialaizer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Review found'})
        else:
            return Response({'status':False,'data':None,'message':'Review not found'})

    def create(self, request, *args, **kwargs):
        data=request.data
        data['user_reviewed']=request.user.id
        serializer=ReviewSerialaizer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'Review Added'})
        else:
            return Response({'status':False,'data':None,'message':'Review cannot add'})
    
    def update(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            data=request.data
            data['user_reviewed']=request.user.id
            serializer=ReviewSerialaizer(instance,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':'Review Changed'})
            else:
                return Response({'status':False,'data':None,'message':'Review cannot Changed'})
        except:
                return Response({'status':False,'data':None,'message':'Review cannot Changed'})

    
    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'Review deleted'})       
        except:
            return Response({'status':False,'data':None,'message':'Review cannot deleted'})       
            
class FavouriteViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=favourite.objects.select_related('user','product').all()
    serializer_class=FavouriteSerializer()
    def list(self, request, *args, **kwargs):
        user=request.user
        queryset=favourite.objects.select_related('user','product').filter(user=user)
        if queryset.exists():
            serializer=FavouriteSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Your favourites'})
        else:
            return Response({'status':False,'data':None,'message':'favourites not found'})

    def create(self, request, *args, **kwargs):
        user=request.user
        data=request.data
        data['user']=user.id
        serializer=FavouriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'Item added to favourite'})
        else:
            return Response({'status':False,'data':None,'message':'Item not added to favourite'})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'Item removed from favourite'})
        except:
            return Response({'status':False,'data':None,'message':'Item cannot removed'})


        


class SpecialOfferViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) & Q(Special_offer=True))

    def list(self, request, *args, **kwargs):
        queryset=Product.objects.select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) & Q(Special_offer=True))
        if queryset.exists():
            serializer=ProductSerialaizer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'special offer found'})
        else:
            return Response({'status':False,'data':None,'message':'special offer not found'})


class toptwospViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) & Q(Special_offer=True))[:2]

    def list(self, request, *args, **kwargs):
        queryset=Product.objects.select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) & Q(Special_offer=True))[:2]
        if queryset.exists():
            serializer=ProductSerialaizer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'top 2 special offer found'})
        else:
            return Response({'status':False,'data':None,'message':'top 2 special offer not found'})

