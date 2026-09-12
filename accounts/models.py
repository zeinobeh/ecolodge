from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):
    pass


class Interests(models.Model):
    name= models.CharField()
    
    def __str__(self):
        return self.name
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(blank=True, verbose_name='نام')
    last_name = models.CharField(blank=True, verbose_name='نام خانوادگی')
    phone_number = models.CharField(max_length=11, blank=True, verbose_name='شماره همراه')
    owner = models.BooleanField( verbose_name="آیا میزبان اقامتگاه هستی؟" ,default=False)
    interests = models.ManyToManyField(Interests , blank=True, verbose_name='علاقه مندی ها')

    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)