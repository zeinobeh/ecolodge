from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login,  logout, get_user_model
from .forms import LoginForm, RegisterForm, ProfileForm, InterestsForm, MyLodgesForm, LodgeImageForm, LodgeImageFormSet
from .models import Profile, User, Interests
from lodges.models import Lodge
from django.views.generic import ListView, DetailView 

from django.contrib import messages


def login_page(request):
    login_form= LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('accounts:dashboard')
        else:
            print('Error')

    context={
        'title': 'صفحه ورود',
        'message': 'ورود',
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
        messages.success(request, "با موفقیت عضو شدید")

    context={
        'title': 'صفحه عضویت',
        'message': 'عضویت',
        'register_form': register_form
    }
    return render(request,'register_page.html',context)


def log_out(request):
    logout(request)
    return redirect('accounts:login')


def dashboard(request):
    context = {
        "welcome": "خوش آمدید",
    }
    return render(request, 'dashboard/dashboard.html', context)


def profile_page(request):
    if request.method == "POST":
        profile_form = ProfileForm(
            request.POST,
            instance=request.user.profile
        )

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "پروفایل آپدیت شد")
            return redirect("accounts:profile")
            
    else:
        profile_form = ProfileForm(
            instance=request.user.profile
        )


    context={'profile_form': profile_form}
    return render(request, "dashboard/profile.html", context)



def interests_page(request):
    if request.method == "POST":
        interests_form = InterestsForm(
            request.POST,
            instance=request.user.profile
        )

        if interests_form.is_valid():
            interests_form.save()
            # user_interest = interests_form.cleaned_data['interests']
            messages.success(request, "علاقه مندی ها ثبت شد")
            return redirect("accounts:interests")

    else:
        interests_form = InterestsForm(
            instance=request.user.profile
        )


    context= {
        "interests_form": interests_form,
    }
    return render(request, "dashboard/interests.html", context)






############################################ مخصوص میزبانان اقامتگاه

def create_lodge(request):
    if request.method == "POST":
        form = MyLodgesForm(request.POST)
        formset = LodgeImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            lodge= form.save(commit=False)
            lodge.owner= request.user
            lodge.save()
            form.save_m2m()
            formset.instance = lodge
            formset.save()
            return redirect("accounts:my_lodges_list")
    else:
        form = MyLodgesForm()
        formset = LodgeImageFormSet()

    context = {
        "message": "ثبت اقامتگاه جدید",
        "form" : form,
        "formset": formset
    }
    return render(request, 'dashboard/create_lodge.html', context)




def edit_lodge(request, id):
    lodge = get_object_or_404( Lodge, id=id, owner=request.user )
    if request.method == "POST":
        form=MyLodgesForm(request.POST, instance=lodge)
        formset = LodgeImageFormSet(request.POST, request.FILES, instance=lodge)
        if form.is_valid() and formset.is_valid():
            lodge= form.save(commit=False)
            lodge.owner= request.user
            lodge.status = 'pending'
            lodge.save()
            form.save_m2m()
            formset.save()
            return redirect("accounts:my_lodges_list")
    else:
        form = MyLodgesForm(instance=lodge)
        formset = LodgeImageFormSet(instance=lodge)

    context = {
        "message": "ویرایش اطلاعات اقامتگاه",
        "form": form,
        "formset": formset
    }
    return render(request, 'dashboard/edit_lodge.html', context)


def delete_lodge(request, id):
    lodge = get_object_or_404( Lodge, id=id, owner=request.user )  
    lodge.delete()
    return redirect('accounts:my_lodges_list')  


class MyLodgesListView(ListView):
    model = Lodge
    template_name = 'dashboard/my_lodges_list.html'
    context_object_name = "lodges"
    paginate_by=10

    def get_queryset(self):
        return Lodge.objects.filter(owner=self.request.user).order_by('-id')
