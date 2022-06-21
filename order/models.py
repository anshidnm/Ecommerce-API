from django.db import models
from django.contrib.auth.models import User
from main.models import Product
from datetime import datetime
from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver


# models

class Address(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_have_address')
    zone=models.CharField(max_length=100)
    area=models.CharField(max_length=100)
    mobile=models.PositiveBigIntegerField()
 
    def __str__(self):
        return self.user.username

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
    bill=models.PositiveIntegerField(default=0)
    is_payment_done=models.BooleanField(default=False)
    def __str__(self):
        return "order_id__{} made by {}".format(self.id,self.cart.user.username)


class Payment(models.Model):
    order=models.ForeignKey(Orders,on_delete=models.CASCADE)
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
        pdt=Product.objects.get(id=i.product.id)
        pdt.stock-=i.quantity
        pdt.save()
        temp=temporaryitem.objects.create(product=i.product,cart=i.cart,quantity=i.quantity,total=i.total)
        temp.save()
    instance.bill=obj.grand_total
    item.delete()


@receiver(sender=Orders,signal=pre_delete)
def order_update(sender,instance,*args,**kwargs):
    obj=cart.objects.get(id=instance.cart.id)
    item=temporaryitem.objects.filter(cart=instance.cart)
    for i in item:
        pdt=Product.objects.get(id=i.product.id)
        pdt.stock+=i.quantity
        pdt.save()
    item.delete()

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
    instance.amount=instance.order.bill
    order_obj=Orders.objects.get(id=instance.order.id)
    order_obj.is_payment_done=True
    order_obj.save()