from django.shortcuts import render, redirect
from lodges.models import Lodge


def header(request):
    context={}
    return render(request,'base/header.html',context)

def footer(request):
    context={}
    return render(request,'base/footer.html',context)



def home_page(request):
    lodges = Lodge.objects.get_showing_lodge()

    context={
        'lodges' : lodges ,
        'message': 'welcome',
    }
    return render(request,'home_page.html',context)



