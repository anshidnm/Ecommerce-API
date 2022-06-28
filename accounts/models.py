import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from datetime import datetime
import os
from django.core.validators import MinLengthValidator


class Image_upload(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='image')
    image=models.ImageField(upload_to='pictures')
    def __str__(self):
        return f"{self.user.username}_image"


def delete_path(imagepath):
    if os.path.isfile(imagepath):
        os.remove(imagepath)

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    title=models.CharField(max_length=100)
    text=models.TextField()
    time=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

class Mobile(models.Model):
    user=models.OneToOneField(User,related_name='mobile',on_delete=models.CASCADE)
    country_code=models.CharField(max_length=5)
    mobile_number=models.PositiveBigIntegerField()

@receiver(signal=pre_delete,sender=Image_upload)
def delete_image(sender,instance,*args,**kwargs):
    if instance.image:
        delete_path(instance.image.path)