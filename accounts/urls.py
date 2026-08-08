from django.urls import path
from .views import  login_page, register_page, log_out, dashboard, profile_page, interests_page, create_lodge, MyLodgesListView, edit_lodge


app_name = "accounts"

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout', log_out, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/profile/', profile_page , name='profile'),
    path('dashboard/interests/', interests_page , name='interests'),
    path('dashboard/create_lodge/', create_lodge , name='create_lodge'),
    path('dashboard/my_lodges_list/', MyLodgesListView.as_view() , name='my_lodges_list'),
    path('dashboard/my_lodges_list/<int:id>/edit/', edit_lodge, name='edit_lodge'),
]


