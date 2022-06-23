from . models import Review,Category,Brand,Product,favourite
from . serializers import ProductSerialaizer,CategorySerialaizer,BrandSerialaizer,ReviewSerialaizer,FavouriteSerializer,FavoriteListSerializer,GrocerySerializer
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
            return Response({'status':True,'data':serializer.data,'message':'Category found'})
        else:
            return Response({'status':False,'data':None,'message':'Category not found'})
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance)
            return Response({'status':True,'data':serializer.data,'message':'Category Found'})
        except:
            return Response({'status':False,'data':None,'message':'Category not Found'})


class BrandViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Brand.objects.filter(active=True)
    serializer_class=BrandSerialaizer

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Brands found'})
        else:
            return Response({'status':False,'data':None,'message':'Brands not found'})
    

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
            return Response({'status':True,'data':serializer.data,'message':'Products found'})
        else:
            return Response({'status':False,'data':None,'message':'Products not found'})
          
    def retrieve(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            serializer=self.get_serializer(instance)
            return Response({'status':True,'data':serializer.data,'message':'product found'})
        except:
            return Response({'status':False,'data':None,'message':'product not found'})


class ReviewViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset=Review.objects.all()
    serializer_class=ReviewSerialaizer
    
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('user_reviewed','product_reviewed')
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Review found'})
        else:
            return Response({'status':False,'data':None,'message':'Review not found'})

    def create(self, request, *args, **kwargs):
        data=request.data
        data['user_reviewed']=request.user.id
        serializer=self.get_serializer(data=data)
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
            serializer=self.get_serializer(instance,data=data)
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
    queryset=favourite.objects.all()
    serializer_class=FavouriteSerializer()
    def list(self, request, *args, **kwargs):
        user=request.user
        queryset=self.get_queryset().select_related('user','product').filter(user=user)
        if queryset.exists():
            serializer=FavoriteListSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Your favourites'})
        else:
            return Response({'status':False,'data':None,'message':'favourites not found'})

    def create(self, request, *args, **kwargs):
        user=request.user
        data=request.data
        data['user']=user.id
        serializer=self.get_serializer(data=data)
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
    queryset=Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) & Q(Special_offer=True))
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'special offer found'})
        else:
            return Response({'status':False,'data':None,'message':'special offer not found'})


class toptwospViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand').filter( Q(active=True) & Q(stock__gt=0) & Q(Special_offer=True))[:2]
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'top 2 special offer found'})
        else:
            return Response({'status':False,'data':None,'message':'top 2 special offer not found'})

class BestSellingViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand').filter(Q(active=True) & Q(stock__gt=0) & Q(order_count__gt=0)).order_by('-order_count')
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'Bestselling found'})
        else:
            return Response({'status':False,'data':None,'message':'Bestselling not found'})

class toptwobsViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=ProductSerialaizer
    queryset=Product.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('category','brand').filter(Q(active=True) & Q(stock__gt=0) & Q(order_count__gt=0)).order_by('-order_count')[:2]
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'top 2 Bestselling found'})
        else:
            return Response({'status':False,'data':None,'message':'top 2 Bestselling not found'})

class GroceryViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=GrocerySerializer
    queryset=Category.objects.filter(active=True)

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset()[:2]
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'top 2 grocery found'})
        else:
            return Response({'status':False,'data':None,'message':'top 2 grocery not found'})
