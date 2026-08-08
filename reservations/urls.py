from django.urls import path
from .views import  resevation_data, ReservesView

app_name = "reservations"

urlpatterns = [
    path('reserve/<int:lodge_id>/', resevation_data, name="reserve"),
    path('reserve/view/', ReservesView.as_view(), name="reserves_view")
]