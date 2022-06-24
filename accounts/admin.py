from django.contrib import admin
from .models import Image_upload,Notification

admin.site.register(Image_upload)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_filter =('user','title')

