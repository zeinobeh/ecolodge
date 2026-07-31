from django.shortcuts import render, redirect
from lodges.models import Lodge
from django.core.paginator import Paginator

def header(request):
    context={}
    return render(request,'base/header.html',context)

def footer(request):
    context={}
    return render(request,'base/footer.html',context)



def home_page(request):
    lodges = Lodge.objects.get_showing_lodge()
    
    paginator=Paginator(lodges, 8)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context={
        'message': 'welcome',
        'page_obj' : page_obj
    }
    return render(request,'home_page.html',context)



