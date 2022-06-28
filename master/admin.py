from django.contrib import admin
from .models import *

@admin.register(MasterProduct)
class MasterProductAdmin(admin.ModelAdmin):
    list_display = ('name','stock','serial_no')
