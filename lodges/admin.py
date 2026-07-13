from django.contrib import admin
from .models import Lodge

# Register your models here.

class LodgeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status' , 'active']
    class Meta:
        model = Lodge

admin.site.register(Lodge, LodgeAdmin)
