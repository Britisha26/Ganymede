from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.utils import timezone
from django.db.models import Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Agent(models.Model):
    user=models.OneToOneField(User,related_name='agent',on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True)
    available=models.BooleanField(default=True,blank=True)
    aadhar=models.IntegerField(unique=True,null=True)
    previous_workplace=models.TextField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    emergency_contact=PhoneField(unique=True,null=True)
    pic=models.ImageField(upload_to='uploads/Agent_pics',blank=True,null=True)
    phone=PhoneField(unique=True,null=True)
    email=models.EmailField(unique=True,null=True)
    vehile_license=models.CharField(max_length=30,null=True)
    rate=models.IntegerField(default=5,validators=[MaxValueValidator(5),MinValueValidator(1)],blank=True,null=True)
    rev=models.ForeignKey("AgentReview",on_delete=models.CASCADE,related_name='agentrev',null=True,blank=True)
    
    @property
    def avgrate(self):
        return AgentRating.objects.filter(rest=self).aggregate(Avg("rating"))
    

class AgentRating(models.Model):
    delagent=models.ForeignKey('Agent',on_delete=models.CASCADE,null=True)
    rating=models.IntegerField(default=5,validators=[MaxValueValidator(5),MinValueValidator(1)],null=True)
    customer=models.ForeignKey("Client.Profile",on_delete=models.CASCADE,null=True)

class AgentReview(models.Model):
    review=models.TextField(null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    rest=models.ForeignKey("Agent",on_delete=models.CASCADE,null=True)
    posted_on=models.DateTimeField(default=timezone.now)
