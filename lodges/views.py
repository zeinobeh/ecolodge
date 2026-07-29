from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from .models import Lodge


# Create your views here.


class LodgesListView(ListView):
    template_name = 'lodges_list.html'
    context_object_name = "lodges"
    paginate_by=5

    def get_queryset(self):
        return Lodge.objects.get_showing_lodge()



class LodgeDetail(DetailView):
    model = Lodge
    template_name = 'Lodge_detail.html'
    context_object_name = "lodge"

    def get_object(self, queryset = Lodge.objects.get_showing_lodge()):
        return super().get_object(queryset)



