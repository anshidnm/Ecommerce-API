from django.contrib import admin
from .models import Product,Category,Brand,Review,favourite


admin.site.register(Brand)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display =('category_name','image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','category','brand','stock','price_per_amount','Special_offer','average','order_count')
    list_filter = ('category','brand','Special_offer')
    search_fields = ('name__contains',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_reviewed','product_reviewed','text','user_opinion')

@admin.register(favourite)
class FavoriteAdmin(admin.ModelAdmin):
    list_filter =('user',)