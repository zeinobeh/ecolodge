from django.urls import path
from .views import  LodgesListView, LodgeDetail

app_name = "lodges"

urlpatterns = [
    path('', LodgesListView.as_view(), name="lodges_list_view"),
    path('<slug>/', LodgeDetail.as_view(), name="lodge_detail"),  
]