from django.shortcuts import render, redirect





def home_page(request):
    context = {
        'message' : "Welcome",
    }
    return render(request , 'home_page.html', context)


