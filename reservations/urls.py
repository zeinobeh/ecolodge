from django.urls import path
from .views import  reservation_data, ReservesView, cancel_reserve

app_name = "reservations"

urlpatterns = [
    path('reserve/view/', ReservesView.as_view(), name="reserves_view"),
    path('reserve/<int:lodge_id>/', reservation_data, name="reserve"),
    path('reserve/cancle/<int:reservation_id>/', cancel_reserve, name="cancel_reserve")
]