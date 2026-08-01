from django.urls import path
from .views import  login_page, register_page, log_out, profile_page, interests_page

app_name = "accounts"

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout', log_out, name='logout'),
    path('dashboard/profile/', profile_page , name='profile'),
    path('dashboard/interests/', interests_page , name='interests'),
]