from django.contrib import admin
from .models import Image_upload,Notification,Mobile

admin.site.register(Image_upload)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_filter =('user','title')

@admin.register(Mobile)
class MobileAdmin(admin.ModelAdmin):
    list_display =('user','country_code','mobile_number')