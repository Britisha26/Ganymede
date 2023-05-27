from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phone_field import PhoneField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Order(models.Model):
    ordered_on=models.DateTimeField(default=timezone.now)
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    items=models.ManyToManyField("MenuItem",blank=True, related_name='menuitem')
    is_paid=models.BooleanField(default=False,blank=True)
    is_sent=models.BooleanField(default=False,blank=True)
    user=models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=30,null=True)
    phone=PhoneField(null=True)
    email=models.EmailField(unique=False,default="someone@gmail.com")
    street=models.CharField(max_length=70,blank=True,null=True)
    area=models.CharField(max_length=70,blank=True,null=True)
    city=models.CharField(max_length=70,blank=True,null=True)
    state=models.CharField(max_length=70,blank=True,null=True)
    pincode=models.IntegerField(blank=True,null=True)
    res=models.ForeignKey("Restaurant.Restaurant",related_name='restaurant',on_delete=models.CASCADE,null=True)


class MenuItem(models.Model):
    name=models.CharField(max_length=60,null=True)
    foodpic=models.ImageField(upload_to='uploads/Food_Items',blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    ingredients=models.TextField(blank=True,null=True)
    available=models.BooleanField(default=False,blank=True)
    nv=models.TextField(choices=[('1','Veg'),('2','NonVeg'),('3','Both')],default='1')
    res=models.ForeignKey("Restaurant.Restaurant",related_name='restro',on_delete=models.CASCADE,null=True)
    category=models.ManyToManyField("Category",related_name='cat')
    
    def _str_(self):
          return self.name
    
class Category(models.Model):
    name=models.CharField(max_length=100)
    def _str_(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='user',primary_key=True,related_name="profile")
    name = models.CharField(max_length=30,null=True)
    role=models.TextField(choices=[('1',"Customer"),('2',"Restaurant")],default='1')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


    
    
class Customer(models.Model):
    user=models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=30,null=True)
    picture=models.ImageField(upload_to='uploads/Customer_pics',blank=True,null=True)
    email = models.EmailField(default="someone@gmail.com",null=True)
    phone=PhoneField(null=True)
    
    street=models.CharField(max_length=70,blank=True,null=True)
    area=models.CharField(max_length=70,blank=True,null=True)
    city=models.CharField(max_length=70,blank=True,null=True)
    state=models.CharField(max_length=70,blank=True,null=True)
    pincode=models.IntegerField(blank=True,null=True)
    allergy=models.TextField(null=True,blank=True)


class FeedBack(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    email = models.EmailField(default="someone@gmail.com")
    name = models.CharField(max_length=30,null=True)
    feedback=models.TextField(null=True)