from django.urls import path
from .views import  login_page, register_page, log_out, dashboard, profile_page, interests_page, my_lodges_page

app_name = "accounts"

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout', log_out, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/profile/', profile_page , name='profile'),
    path('dashboard/interests/', interests_page , name='interests'),
    path('dashboard/my_lodges/', my_lodges_page , name='my_lodges'),
]