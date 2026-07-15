from django.contrib import admin
from .models import Lodge, LodgeImage

# Register your models here.

class LodgeImageInline(admin.TabularInline):
    model = LodgeImage
    extra = 1          # تعداد فیلدهای خالی که نمایش داده شود
    # max_num = 4      # حداکثر تعداد رکورد مجاز
    # min_num = 1        # حداقل تعداد رکورد (اجباری)
    fields = ['image'] # فیلدهایی که نمایش داده شوند
    can_delete = True  # اجازه حذف رکوردها (پیش‌فرض True)
    


class LodgeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'city' , 'price','status', 'active']
    list_filter = ['status' , 'active']
    list_per_page = 20

    inlines = [LodgeImageInline]

    class Meta:
        model = Lodge
    






admin.site.register(Lodge, LodgeAdmin)
