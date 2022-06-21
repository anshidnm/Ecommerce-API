from django.contrib import admin
from . models import cart,cartItem,Orders,Address,Payment,temporaryitem

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display =('user','zone','area','mobile')

@admin.register(cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user','grand_total')
    readonly_fields = ('grand_total',)

@admin.register(cartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart','product','quantity','total')
    list_filter = ('cart',)
    readonly_fields = ('total',)

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('bill',)
   
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display =('order','amount','user','made_on')
    readonly_fields = ('user','amount')

admin.site.register(temporaryitem)