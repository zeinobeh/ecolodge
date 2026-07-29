from django.shortcuts import render, redirect


def header(request):
    context={}
    return render(request,'base/header.html',context)

def footer(request):
    context={}
    return render(request,'base/footer.html',context)



def home_page(request):
    context={
        'message': 'welcome',
    }
    return render(request,'home_page.html',context)



