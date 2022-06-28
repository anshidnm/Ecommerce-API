from django.contrib import admin
from . models import cart,cartItem,Orders,Address,Payment,temporaryitem,Payment_method,Delivery_method,Promocode

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display =('user','zone','area')

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
    list_display = ('cart','amount_to_pay','amount_paid','is_payment_done')
    readonly_fields = ('amount_to_pay','amount_paid')
   
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display =('order','amount','user','made_on')
    readonly_fields = ('user','amount')

admin.site.register(temporaryitem)
admin.site.register(Payment_method)
admin.site.register(Delivery_method)
admin.site.register(Promocode)