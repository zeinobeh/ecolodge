from django.contrib import admin
from .models import Reservation

# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'lodge' , 'guest_count','check_in', 'check_out', 'status']
    list_per_page = 20

admin.site.register(Reservation, ReservationAdmin)