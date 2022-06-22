from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os

class Image_upload(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='image')
    image=models.ImageField(upload_to='pictures',default='./static/img/team_4.jpg')
    def __str__(self):
        return self.user.username


def delete_path(imagepath):
    if os.path.isfile(imagepath):
        os.remove(imagepath)


@receiver(signal=pre_delete,sender=Image_upload)
def delete_image(sender,instance,*args,**kwargs):
    if instance.image:
        delete_path(instance.image.path)