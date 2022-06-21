import email
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser,AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer

class RegisterViewset(viewsets.ModelViewSet):
    permission_classes=[AllowAny]
    queryset=User.objects.all()
    serializer_class=UserSerializer

    def list(self, request, *args, **kwargs):
        queryset=User.objects.all()
        if queryset.exists():
            serializer=UserSerializer(queryset,many=True)
            return Response({'status':True,'data':serializer.data,'message':'user found'})
        else:
            return Response({'status':False,'data':None,'message':'user not found'})
