import imp
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response

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


