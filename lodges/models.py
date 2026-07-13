from django.db import models
from django.utils.text import slugify

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Q

# Create your models here.

class LodgeManager(models.Manager):
    def get_active_lodge(self):
        return self.get_queryset().filter(active = True, status='')
    
#     def search_lodge(self,query):
#         lookup = Q(title__icontains=query) | Q(description__icontains=query)
#         return self.get_queryset().filter(lookup, active=True)



class Lodge(models.Model):
    STATUS_CHOICES= [
        ('pending', 'در انتظار تایید'),
        ('confirmed', 'تایید شده'),
        ('canclled', 'رد شده'),
    ]

    # owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='عنوان')
    slug= models.SlugField(blank=True, unique=True, allow_unicode=True)
    description = models.TextField()
    province = models.CharField()
    city = models.CharField()
    address = models.TextField()
    capacity = models.IntegerField()
    price = models.IntegerField()
    active = models.BooleanField(default=True)
    status = models.CharField(choices=STATUS_CHOICES, default='pending')
    

    # objects= LodgeManager()

    class Meta:
        verbose_name= 'اقامتگاه'
        verbose_name_plural= 'اقامتگاه ها'

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':
            raw_slug = slugify(self.title, allow_unicode=True)
            self.slug = raw_slug
        super().save(*args, **kwargs)

    def lodge_url(self):
        return f"/lodge/{self.slug}"

    def __str__(self):
        return self.title
    

@receiver(pre_save, sender=Lodge)
def create_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug = slugify(instance.title)
        # اطمینان از یکتایی
        unique_slug = slug
        counter = 1
        while Lodge.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{counter}"
            counter += 1
        instance.slug = unique_slug






class LodgeImage(models.Model):
    lodge= models.ForeignKey(Lodge, on_delete=models.CASCADE)
    # image= models.ImageField(upload_to="/lodgeimages", null=True , blank=True)

