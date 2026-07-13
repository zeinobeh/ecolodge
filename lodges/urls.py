from django.urls import path
from .views import  LodgesListView

app_name = "lodges"

urlpatterns = [
    path('', LodgesListView.as_view(), name="lodges_list_view"),
    # path('<slug>', ProductDetail.as_view(),name="detail"),
    
]