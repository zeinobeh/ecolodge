from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass


class Interest(models.Model):
    name= models.CharField()
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField()
    last_name = models.CharField()
    phone_number = models.CharField(max_length=11)
    owner = models.BooleanField(default=False)
    interests = models.ManyToManyField(Interest , blank=True)