
from constantVariables import *
from . models import Review,Category,Brand,Product,favourite
from . serializers import ProductSerialaizer,CategorySerialaizer,BrandSerialaizer,ReviewSerialaizer,FavouriteSerializer,FavoriteListSerializer,GrocerySerializer,ProductShortSerializer
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
        queryset=self.get_queryset().prefetch_related(Prefetch('productshavecategory',Product.objects.all()))
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':CATEGORY_FOUND})
        else:
            return Response({'status':False,'data':None,'message':CATEGORY_NOT_FOUND})
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance)
            return Response({'status':True,'data':serializer.data,'message':CATEGORY_FOUND})
        except:
            return Response({'status':False,'data':None,'message':CATEGORY_NOT_FOUND})


class BrandViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Brand.objects.filter(active=True)
    serializer_class=BrandSerialaizer

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':BRAND_FOUND})
        else:
            return Response({'status':False,'data':None,'message':BRAND_NOT_FOUND})
    

class ProductViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Product.objects.filter( Q(active=True) & Q(stock__gt=0) )
    serializer_class=ProductSerialaizer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ['category','brand']

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand')
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':PRODUCT_FOUND})
        else:
            return Response({'status':False,'data':None,'message':PRODUCT_NOT_FOUND})
          
    def retrieve(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance)
            return Response({'status':True,'data':serializer.data,'message':PRODUCT_FOUND})
        except:
            return Response({'status':False,'data':None,'message':PRODUCT_NOT_FOUND})


class ReviewViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Review.objects.all()
    serializer_class=ReviewSerialaizer
    
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('user_reviewed','product_reviewed')
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':REVIEW_FOUND})
        else:
            return Response({'status':False,'data':None,'message':REVIEW_NOT_FOUND})

    def create(self, request, *args, **kwargs):
        data=request.data
        data['user_reviewed']=request.user.id
        serializer=self.get_serializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':REVIEW_ADDED})
            else:
                return Response({'status':False,'data':None,'message':REVIEW_NOT_ADDED})
        except:
            return Response({'status':False,'data':None,'message':REVIEW_NOT_ADDED})

    
    def update(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            data=request.data
            data['user_reviewed']=request.user.id
            serializer=self.get_serializer(instance,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':REVIEW_CHANGED})
            else:
                return Response({'status':False,'data':None,'message':REVIEW_NOT_CHANGED})
        except:
                return Response({'status':False,'data':None,'message':REVIEW_NOT_CHANGED})

    
    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':REVIEW_DELETED})       
        except:
            return Response({'status':False,'data':None,'message':REVIEW_NOT_DELETED})       
            
class FavouriteViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=favourite.objects.all()
    serializer_class=FavouriteSerializer()
    def list(self, request, *args, **kwargs):
        user=request.user
        queryset=self.get_queryset().select_related('user','product').filter(user=user)
        if queryset.exists():
            serializer=FavoriteListSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':FAVOURITE_FOUND})
        else:
            return Response({'status':False,'data':None,'message':FAVOURITE_NOT_FOUND})

    def create(self, request, *args, **kwargs):
        user=request.user
        data=request.data
        data['user']=user.id
        serializer=self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':FAVOURITE_ADDED})
        else:
            return Response({'status':False,'data':None,'message':FAVOURITE_NOT_ADDED})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':FAVOURITE_DELETED})
        except:
            return Response({'status':False,'data':None,'message':FAVOURITE_NOT_DELETED})


        


class SpecialOfferViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) & Q(Special_offer=True))
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':SPECIAL_OFFER_FOUND})
        else:
            return Response({'status':False,'data':None,'message':SPECIAL_OFFER_NOT_FOUND})


class toptwospViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) & Q(Special_offer=True))[:2]
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':SPECIAL_OFFER_FOUND})
        else:
            return Response({'status':False,'data':None,'message':SPECIAL_OFFER_NOT_FOUND})

class BestSellingViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand').filter(Q(active=True) & Q(stock__gt=0) & Q(order_count__gt=0)).order_by('-order_count')
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':BEST_SELLING_FOUND})
        else:
            return Response({'status':False,'data':None,'message':BEST_SELLING_NOT_FOUND})

class toptwobsViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand').filter(Q(active=True) & Q(stock__gt=0) & Q(order_count__gt=0)).order_by('-order_count')[:2]
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':BEST_SELLING_FOUND})
        else:
            return Response({'status':False,'data':None,'message':BEST_SELLING_NOT_FOUND})

class GroceryViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=GrocerySerializer
    queryset=Category.objects.filter(active=True)

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()[:2]
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':CATEGORY_FOUND})
        else:
            return Response({'status':False,'data':None,'message':CATEGORY_NOT_FOUND})

class SpecificReviewViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ReviewSerialaizer
    queryset=Review.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('user_reviewed','product_reviewed').filter(product_reviewed=request.data['product_reviewed'])
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':REVIEW_FOUND})
        else:
            return Response({'status':False,'data':None,'message':REVIEW_NOT_FOUND})
