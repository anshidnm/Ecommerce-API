from dataclasses import fields
import imp
from pyexpat import model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image_upload
    
class UserSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(write_only=True)
    class Meta:
        model=User
        exclude=('password',)

    def validate(self, data):
        if len(data["password2"]) < 8:
            raise serializers.ValidationError("Password must be atleast 8 characters")
        return data

    def create(self,validated_data):
        user = User.objects.create(username=validated_data["username"],email=validated_data["email"],)
        user.set_password(validated_data["password2"])
        user.save()
        return user

class ImageSerializer(serializers.ModelSerializer):
    user_details=serializers.SerializerMethodField()
    def get_user_details(self,obj):
        user_obj=User.objects.get(id=obj.user.id)
        nested_user_serializer=UserSerializer(user_obj)
        return nested_user_serializer.data
    
    class Meta:
        model=Image_upload
        fields="__all__"
