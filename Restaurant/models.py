from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phone_field import PhoneField
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Restaurant(models.Model):
    lic=models.IntegerField(null=True)
    name=models.CharField(max_length=70,null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    pic=models.ImageField(upload_to='uploads/Restaurant_pics',blank=True,null=True)
    phone=PhoneField(unique=True,null=True)
    email=models.EmailField(unique=True,null=True)
    cuisine= models.CharField(max_length=40, blank=True, null=True)
    address= models.TextField(null=True)
    nv=models.TextField(choices=[('1','Veg'),('2','NonVeg'),('3','Both')],default='1')
    rate=models.IntegerField(default=5,validators=[MaxValueValidator(5),MinValueValidator(1)],blank=True,null=True)
    rev=models.ForeignKey("RestaurantReview",on_delete=models.CASCADE,related_name='rev',null=True,blank=True)
    
    @property
    def avgrate(self):
        return Rating.objects.filter(rest=self).aggregate(Avg("rating"))
    

class Rating(models.Model):
    rest=models.ForeignKey('Restaurant',on_delete=models.CASCADE,null=True)
    rating=models.IntegerField(default=5,validators=[MaxValueValidator(5),MinValueValidator(1)],null=True)
    customer=models.ForeignKey("Client.Profile",on_delete=models.CASCADE,null=True)

class RestaurantReview(models.Model):
    review=models.TextField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    rest=models.ForeignKey("Restaurant",on_delete=models.CASCADE,null=True)
    posted_on=models.DateTimeField(default=timezone.now)