from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response

from .models import Image_upload
from .serializers import UserSerializer,ImageSerializer


class RegisterViewset(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=User.objects.select_related('user_have_address').all()
    serializer_class=UserSerializer

    def list(self, request, *args, **kwargs):
        queryset=User.objects.select_related('user_have_address').all()
        if queryset.exists():
            serializer=UserSerializer(queryset,many=True)
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
            serializer=ImageSerializer(queryset)
            return Response({'status':True,'data':serializer.data,'message':'profile found'})
        except:
            return Response({'status':False,'data':None,'message':'profile not found'})
    def create(self, request, *args, **kwargs):
        data=request.data
        data['user']=request.user.id
        serializer=ImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':True,'data':serializer.data,'message':'profile created'})
        else:
            return Response({'status':False,'data':None,'message':'profile not created'})

    def update(self, request, *args, **kwargs):
        try:
            data=request.data
            data['user']=request.user.id
            instance=self.get_object()
            serializer=ImageSerializer(instance,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'data':serializer.data,'message':'profile updated'})
            else:
                return Response({'status':False,'data':None,'message':'profile not updated'})
        except:
            return Response({'status':False,'data':None,'message':'profile not updated'})

    def destroy(self, request, *args, **kwargs):
        try:
            instance=self.get_object()
            instance.delete()
            return Response({'status':True,'data':None,'message':'profile deleted'})
        except:
            return Response({'status':False,'data':None,'message':'profile not deleted'})

 