from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,  logout, get_user_model
from .forms import LoginForm, RegisterForm, ProfileForm, InterestsForm
from .models import Profile, User

def login_page(request):
    login_form= LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            print('Error')

    context={
        'title': 'login page',
        'message': 'Login',
        'login_form': login_form
    }
    return render(request,'login_page.html',context)



User = get_user_model()

def register_page(request):
    register_form= RegisterForm(request.POST or None)
    if register_form.is_valid():
        username = register_form.cleaned_data.get('username')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        User.objects.create_user(username=username,email=email,password=password)

    context={
        'title': 'register page',
        'message': 'register',
        'register_form': register_form
    }
    return render(request,'register_page.html',context)


def log_out(request):
    logout(request)
    return redirect('accounts:login')



def profile_page(request):
    if request.method == "POST":
        profile_form = ProfileForm(
            request.POST,
            instance=request.user.profile
        )

        if profile_form.is_valid():
            profile_form.save()

    else:
        profile_form = ProfileForm(
            instance=request.user.profile
        )

    return render(request, "dashboard/profile.html", {
        "profile_form": profile_form
    })



def interests_page(request):
    if request.method == "POST":
        interests_form = InterestsForm(
            request.POST,
            instance=request.user.profile
        )

        if interests_form.is_valid():
            interests_form.save()

    else:
        interests_form = InterestsForm(
            instance=request.user.profile
        )
    return render(request, "dashboard/interests.html", {
        "interests_form": interests_form
    })