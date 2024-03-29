from django.db import models
from django.contrib.auth.models import User
from main.models import Product
from datetime import datetime
from django.db.models.signals import pre_save,pre_delete,post_save
from django.dispatch import receiver
from accounts.models import Notification
from master.models import MasterProduct



# models

class Delivery_method(models.Model):
    method=models.CharField(max_length=100)

    def __str__(self):
        return self.method

class Payment_method(models.Model):
    method_of_payment=models.CharField(max_length=100)

    def __str__(self):
        return self.method_of_payment

class Promocode(models.Model):
    name=models.CharField(max_length=100)
    discount=models.IntegerField(default=0)

    def __str__(self):
        return self.name



class Address(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_have_address')
    zone=models.CharField(max_length=100)
    area=models.CharField(max_length=100)
 
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"


class cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)
    grand_total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username

class cartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(cart,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    total=models.PositiveIntegerField(default=0)

    class Meta:
        unique_together=('cart','product',)

    def __str__(self):
        return "{} added {}".format(self.product.name,self.cart.user.username)

class Orders(models.Model):
    cart=models.ForeignKey(cart,on_delete=models.CASCADE)
    amount_to_pay=models.PositiveIntegerField(default=0)
    amount_paid=models.PositiveBigIntegerField(default=0)
    is_payment_done=models.BooleanField(default=False)
    amount_paid=models.PositiveBigIntegerField(default=0)
    address=models.ForeignKey(Address,on_delete=models.CASCADE,default=1)
    delivery_method=models.ForeignKey(Delivery_method,on_delete=models.CASCADE,default=1)
    payment_method=models.ForeignKey(Payment_method,on_delete=models.CASCADE,default=1)
    promocode=models.ForeignKey(Promocode,on_delete=models.CASCADE,blank=True,null=True,default=0)
    def __str__(self):
        return "order_id__{} made by {}".format(self.id,self.cart.user.username)

    class Meta:
        verbose_name_plural = "Orderes"


class Payment(models.Model):
    order=models.OneToOneField(Orders,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    amount=models.IntegerField(blank=True)
    made_on=models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return "{} paid {}".format(self.user.username,self.amount)

class temporaryitem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(cart,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField()
    total=models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.product.name}__{self.cart.user.username}"

#Order reciever

@receiver(sender=Orders,signal=pre_save)
def order_update(sender,instance,*args,**kwargs):
    obj=cart.objects.get(id=instance.cart.id)
    item=cartItem.objects.filter(cart=instance.cart)
    for i in item:
        master_pdt=MasterProduct.objects.get(id=i.product.master_product.id)
        pdt=Product.objects.get(id=i.product.id)
        master_pdt.stock-=i.quantity
        master_pdt.save()
        pdt.order_count+=1
        pdt.save()
        temp=temporaryitem.objects.create(product=i.product,cart=i.cart,quantity=i.quantity,total=i.total)
        temp.save()
    if instance.promocode:
        discount=instance.promocode.discount/100
        discount_amount=obj.grand_total*discount
        instance.amount_to_pay=obj.grand_total-discount_amount
    else:
        instance.amount_to_pay=obj.grand_total
    item.delete()
    notification=Notification.objects.create(user=instance.cart.user,title="Order Placed",text="Your order has been placed successfully")
    notification.save()

@receiver(sender=Orders,signal=pre_delete)
def order_update(sender,instance,*args,**kwargs):
    item=temporaryitem.objects.filter(cart=instance.cart)
    for i in item:
        master_pdt=MasterProduct.objects.get(id=i.product.master_product.id)
        pdt=Product.objects.get(id=i.product.id)
        master_pdt.stock+=i.quantity
        master_pdt.save()
        pdt.order_count-=1
        pdt.save()
    item.delete()
    notification=Notification.objects.create(user=instance.cart.user,title="Order Cancelled",text="Your order has been cancelled")
    notification.save()


#item reciever

@receiver(sender=cartItem,signal=pre_save)
def update_cart(sender,instance,*args,**kwargs):
    instance.total = instance.product.price * instance.quantity
    obj=cart.objects.get(id=instance.cart.id)
    if instance.id == None:
        obj.grand_total += instance.total
        obj.save()
    else:
        prev=cartItem.objects.get(id=instance.id)
        prev_total=prev.total
        obj.grand_total -= prev_total
        obj.grand_total += instance.total
        obj.save()

@receiver(sender=cartItem,signal=pre_delete)
def update_cart(sender,instance,*args,**kwargs):
    obj=cart.objects.get(id=instance.cart.id)
    obj.grand_total -= instance.total
    obj.save()

#payment reciever

@receiver(sender=Payment,signal=pre_save)
def update_payment(sender,instance,*args,**kwargs):
    instance.user=instance.order.cart.user
    instance.amount=instance.order.amount_to_pay
    order_obj=Orders.objects.get(id=instance.order.id)
    order_obj.is_payment_done=True
    order_obj.save()

@receiver(sender=Payment,signal=post_save)
def update_order_bill(sender,instance,*args,**kwargs):
    order_obj=Orders.objects.get(id=instance.order.id)
    order_obj.amount_paid=instance.amount
    order_obj.save()
    notification=Notification.objects.create(user=instance.user,title="Payment Done",text="You paid successfully")
    notification.save()

@receiver(sender=Payment,signal=pre_delete)
def cancel_payment(sender,instance,*args,**kwargs):
    notification=Notification.objects.create(user=instance.user,title="Payment Refund",text="Your payment will be refunded soon")
    notification.save()
