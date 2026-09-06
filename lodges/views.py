from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from .models import Lodge
from .choices import PROVINCES
from reservations.forms import ReservationForm
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.db.models import Q
from datetime import datetime
from django.db.models import Case, When

# Create your views here.

#امتیازدهی به اقامتگاه براساس کاربر
def get_score(request, lodge):
    user = request.user
    user_interest = set(user.profile.interests.values_list("name" , flat=True) )
    lodge_interest = set( lodge.interests.values_list("name" , flat=True))    
    common = lodge_interest & user_interest
    return len(common)

#برگرداندن لیستی مرتب از آیدی اقامتگاه ها برا اساس علایق کاربر
def recommend(request, queryset):
    if not request.user.is_authenticated:
        return []
    score = []
    for lodge in queryset :
        check_score = get_score(request,lodge)
        if check_score > 0 :
            score += [(lodge.id , check_score )]
     
    res = sorted(score, key=lambda x: x[1] , reverse=True)
    return [item[0] for item in res]


# نمایش اقامتگاه ها و سرچ در آنها
class LodgesListView(ListView):
    model = Lodge
    template_name = 'lodges_list.html'
    context_object_name = "lodges"
    paginate_by=12



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["provinces"] = PROVINCES
        return context


    def get_queryset(self):
        queryset = Lodge.objects.filter(active = True, status='confirmed').order_by('-id')      #نمایش اقامتگاه هایی که همه کابران میتوانند ببینند


        pk_list = recommend(self.request, queryset)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pk_list)])
        queryset = queryset.filter(pk__in=pk_list).order_by(preserved)

        query = self.request.GET.get('q')
        if query :
            lookup = Q(title__icontains=query) | Q(description__icontains=query)
            queryset = queryset.filter(lookup)

        province=self.request.GET.get("province")
        if province:
            queryset = queryset.filter(province=province)

        city=self.request.GET.get("city")
        if city:
            queryset = queryset.filter(city=city)

        guest_count=self.request.GET.get("guest_count")
        if guest_count:
            queryset = queryset.filter(capacity__gte=guest_count)

        price = self.request.GET.get("price")
        if price:
            queryset = queryset.filter(price__lte=price)

        check_in = self.request.GET.get("check_in")
        check_out = self.request.GET.get("check_out")
        if check_in and check_out :
            check_in = datetime.strptime(check_in, "%Y/%m/%d").date()
            check_out = datetime.strptime(check_out, "%Y/%m/%d").date()
            queryset = queryset.exclude(
                lodge_reserve__check_in__lte = check_out,
                lodge_reserve__check_out__gte = check_in,
            )                    

        return queryset 







class LodgeDetail(DetailView):
    model = Lodge
    template_name = 'lodge_detail.html'
    context_object_name = "lodge"

    def get_object(self, queryset = None):
        slug = self.kwargs.get('slug')

        lodge = get_object_or_404(Lodge, slug=slug)

        if lodge.active and lodge.status == "confirmed" :
            return lodge
        if lodge.owner == self.request.user or self.request.user.is_staff :
            return lodge
        raise Http404("شما دسترسی به این صفحه ندارید")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReservationForm()
        return context
    