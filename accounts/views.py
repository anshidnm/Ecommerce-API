from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from django.db.models import Prefetch
from .models import Image_upload,Notification
from .serializers import UserSerializer,ImageSerializer,UserShortSerializer,NotificationSerializer
from constantVariables import *

class RegisterViewset(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('user_have_address')
        if queryset.exists():
            serializer=UserShortSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':USER_FOUND})
        else:
            return Response({'status':False,'data':None,'message':USER_NOT_FOUND})

    def create(self, request, *args, **kwargs):
        data=request.data
        password_entry=data['password']
        if len(password_entry) < 8:
            return Response({'status':False,'data':None,'message':PASSWORD_VALIDATION})
        else:
            serializer=UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':None,'message':USER_CREATED})
            else:
                return Response({'status':False,'data':None,'message':USER_NOT_CREATED})


class ImageViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    queryset=Image_upload.objects.all()
    serializer_class=ImageSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset=Image_upload.objects.get(id=request.user.image.id)
            serializer=self.get_serializer(queryset)
            return Response({'status':True,'data':serializer.data,'message':IMAGE_FOUND})
        except:
            return Response({'status':False,'data':None,'message':IMAGE_NOT_FOUND})
    def create(self, request, *args, **kwargs):
        data=request.FILES
        data['user']=request.user.id
        serializer=self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':IMAGE_CREATED})
        else:
            return Response({'status':False,'data':None,'message':IMAGE_NOT_CREATED})

    def update(self, request, *args, **kwargs):
        try:
            data=request.data
            data['user']=request.user.id
            instance=self.get_object()
            serializer=self.get_serializer(instance,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':IMAGE_UPDATED})
            else:
                return Response({'status':False,'data':None,'message':IMAGE_NOT_UPDATED})
        except:
            return Response({'status':False,'data':None,'message':IMAGE_NOT_UPDATED})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':IMAGE_DELETED})
        except:
            return Response({'status':False,'data':None,'message':IMAGE_NOT_DELETED})

class UserShortViewset(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    serializer_class=UserShortSerializer
    queryset=User.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            queryset=User.objects.get(id=request.user.id)
            serializer=self.get_serializer(queryset)
            return Response({'status':True,'data':serializer.data,'message':PROFILE_FOUND})
        except:
            return Response({'status':True,'data':None,'message':PROFILE_NOT_FOUND})

class NotificationViewset(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class=NotificationSerializer
    queryset=Notification.objects.all()

    def list(self, request, *args, **kwargs):
        queryset=self.get_queryset().select_related('user').filter(user=request.user)
        if queryset.exists():
            serializer=NotificationSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':NOTIFICATION_FOUND})
        else:
            return Response({'status':False,'data':None,'message':NOTIFICATION_NOT_FOUND})
    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':NOTIFICATION_DELETED})
        except:
            return Response({'status':False,'data':None,'message':NOTIFICATION_NOT_DELETED})
