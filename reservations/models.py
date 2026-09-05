from django.db import models
from django.conf import settings
from lodges.models import Lodge

# Create your models here.

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reserve')
    lodge = models.ForeignKey(Lodge, on_delete=models.CASCADE, related_name='lodge_reserve')
    guest_count = models.PositiveIntegerField(verbose_name="تعداد مسافران")
    check_in = models.DateField(verbose_name="تاریخ ورود")
    check_out = models.DateField(verbose_name="تاریخ خروج")
    total_price = models.PositiveIntegerField(verbose_name="قیمت نهایی")
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

