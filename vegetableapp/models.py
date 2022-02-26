from django.db import models
from django.utils import timezone

class ModelVegetable(models.Model):
    id = models.AutoField(primary_key=True)
    vegetable_label = models.IntegerField()
    vegetable_name = models.CharField(max_length=50)
    vegetable_price_firsthalf = models.CharField(max_length=100)
    vegetable_price_secondhalf = models.CharField(max_length=100)
    vegetable_price_info = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return f'{self.vegetable_label}, {self.vegetable_name}'

class ModelImage(models.Model):
    image = models.ImageField(upload_to='documents/')
