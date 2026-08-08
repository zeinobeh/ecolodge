from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from .models import Lodge
from django.shortcuts import get_object_or_404
from django.http import Http404

# Create your views here.


class LodgesListView(ListView):
    template_name = 'lodges_list.html'
    context_object_name = "lodges"
    paginate_by=12

    def get_queryset(self):
        return Lodge.objects.get_showing_lodge()



class LodgeDetail(DetailView):
    model = Lodge
    template_name = 'Lodge_detail.html'
    context_object_name = "lodge"

    def get_object(self, queryset = None):
        slug = self.kwargs.get('slug')

        lodge = get_object_or_404(Lodge, slug=slug)

        if lodge.active and lodge.status == "confirmed" :
            return lodge
        if lodge.owner == self.request.user or self.request.user.is_staff :
            return lodge
        raise Http404("شما دسترسی به این صفحه ندارید")



