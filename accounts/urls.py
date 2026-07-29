from django.urls import path
from .views import  login_page, register_page, log_out

app_name = "accounts"

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout', log_out, name='logout'),
]