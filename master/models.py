from django.db import models

class MasterProduct(models.Model):
    name=models.CharField(max_length=100)
    serial_no=models.PositiveIntegerField()
    stock=models.PositiveBigIntegerField(default=0)
    def __str__(self):
        return self.name


