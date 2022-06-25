from distutils.command.upload import upload
from email.policy import default
from statistics import mode
from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver


class Category(models.Model):
    category_name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='categories',default='/static/img/team_4.jpg')
    active=models.BooleanField(default=True)

    def delete(self):
        self.active=False
        self.save(update_fields=('active',))

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    brand_name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='brands',default='/static/img/team_4.jpg')
    active=models.BooleanField(default=True)

    def delete(self):
        self.active=False
        self.save(update_fields=('active',))


    def __str__(self):
        return self.brand_name

class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField()
    details=models.TextField()
    image=models.ImageField(upload_to='products',default='/static/img/team_4.jpg')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='productshavecategory')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='productshavebrand')
    stock=models.PositiveBigIntegerField()
    nutritions=models.TextField(default="vitamin C")
    nutritions_per_amount=models.CharField(max_length=10,default="1kg")
    price_per_amount=models.CharField(max_length=100)
    rating=models.PositiveIntegerField(default=0)
    active=models.BooleanField(default=True)
    Special_offer=models.BooleanField(default=False)
    order_count=models.PositiveIntegerField(default=0)
    rating_count=models.PositiveIntegerField(default=0)
    average=models.FloatField(default=0)

    def delete(self):
        self.active=False
        self.save(update_fields=('active',))
    
    def __str__(self):
        return self.name

class Review(models.Model):
    review_choice=(('1','1'),('2','2'),('3','3'),('4','4'),('5','5'))
    user_reviewed=models.ForeignKey(User,on_delete=models.CASCADE)
    product_reviewed=models.ForeignKey(Product,on_delete=models.CASCADE)
    text=models.CharField(max_length=1,choices=review_choice)
    user_opinion=models.TextField(blank=True)

    class Meta:
        unique_together=('user_reviewed','product_reviewed',)

    def __str__(self):
        return "{} review by {}".format(self.product_reviewed,self.user_reviewed)

class favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='favouritesP')
    class Meta:
        unique_together=('user','product',)

    def __str__(self):
        return "{} likes {}".format(self.user,self.product)


@receiver(sender=Review,signal=pre_save)
def update_review(sender,instance,*args,**kwargs):
    rate=instance.text
    rate_int=int(rate)
    pdts=Product.objects.get(id=instance.product_reviewed.id)
    if instance.id == None:
        pdts.rating_count+=1
        pdts.rating+=rate_int
        pdts.average=pdts.rating/pdts.rating_count
        pdts.save()
    else:
        prev=Review.objects.get(id=instance.id)
        prev_rate=int(prev.text)
        pdts.rating-=prev_rate
        pdts.rating+=rate_int
        pdts.average=pdts.rating/pdts.rating_count
        pdts.save()


@receiver(sender=Review,signal=pre_delete)
def update_review(sender,instance,*args,**kwargs):
    rate=instance.text
    rate_int=int(rate)
    pdts=Product.objects.get(id=instance.product_reviewed.id)
    pdts.rating_count-=1
    pdts.rating-=rate_int
    if pdts.rating_count>0:
        pdts.average=pdts.rating/pdts.rating_count
    else:
        pdts.average=0
    pdts.save()