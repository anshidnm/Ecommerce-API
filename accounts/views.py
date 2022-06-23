from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.db.models import Prefetch

from .models import Image_upload
from .serializers import UserSerializer,ImageSerializer


class RegisterViewset(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('user_have_address')
        if queryset.exists():
            serializer=self.get_serializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'user found'})
        else:
            return Response({'status':False,'data':None,'message':'user not found'})

class ImageViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Image_upload.objects.all()
    serializer_class=ImageSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset=Image_upload.objects.get(id=request.user.image.id)
            serializer=self.get_serializer(queryset)
            return Response({'status':True,'data':serializer.data,'message':'profile image found'})
        except:
            return Response({'status':False,'data':None,'message':'profile image not found'})
    def create(self, request, *args, **kwargs):
        data=request.data
        data['user']=request.user.id
        serializer=self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'profile image created'})
        else:
            return Response({'status':False,'data':None,'message':'profile image not created'})

    def update(self, request, *args, **kwargs):
        try:
            data=request.data
            data['user']=request.user.id
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':'profile image updated'})
            else:
                return Response({'status':False,'data':None,'message':'profile image not updated'})
        except:
            return Response({'status':False,'data':None,'message':'profile image not updated'})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'profile image deleted'})
        except:
            return Response({'status':False,'data':None,'message':'profile image not deleted'})

