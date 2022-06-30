
from dataclasses import fields
from pyexpat import model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Image_upload,Mobile,Notification
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=('password',)
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Image_upload
        fields="__all__"

class UserShortSerializer(serializers.ModelSerializer):
    image=ImageSerializer()
    class Meta:
        model=User
        fields=['id','username','email','image']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields=['id','title','text']

class MobileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Mobile
        fields="__all__"

class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude=('password',)


@receiver(signal=post_save,sender=User)
def create_notification(sender,instance,*args,**kwargs):
    notification=Notification.objects.create(user=instance,title="Welcome",text="Welcome To Shop App. Purchase your First Item...!")
    notification.save()

