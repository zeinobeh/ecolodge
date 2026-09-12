from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from .models import Profile
from lodges.models import Lodge , LodgeImage


class LoginForm(forms.Form):
    username = forms.CharField(
        label = "نام کاربری",
        widget = forms.TextInput(attrs={'maxlength':'150'})
    )
    password = forms.CharField(
        label = "رمز عبور",
        widget= forms.PasswordInput()
    )


User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(
        label = "نام کاربری",
        widget = forms.TextInput(attrs={'maxlength':'150'})
    )
    email = forms.EmailField(
        label = "ایمیل",
        widget = forms.EmailInput()
    )
    password = forms.CharField(
        label = "رمزعبور",
        widget= forms.PasswordInput()
    )
    password2 = forms.CharField(
        label= 'تکرار رمزعبور',
        widget= forms.PasswordInput()
    )

    def clean(self):
        data = self.cleaned_data
        password= self.cleaned_data.get('password')
        password2= self.cleaned_data.get('password2')
        if password != password2 :
            raise forms.ValidationError('پسوردها همخوانی ندارند')
        return data


    def clean_username(self):
        username=self.cleaned_data.get('username')
        query=User.objects.filter(username=username)   
        if query.exists():
            raise forms.ValidationError('نام کاربری دیگری انتخاب نمایید.')
        return username 

    def clean_email(self):
        email=self.cleaned_data.get('email')
        query=User.objects.filter(email=email)   
        if query.exists():
            raise forms.ValidationError('این ایمیل قبلا استفاده شده است.')
        return email
    



class ProfileForm(forms.ModelForm):
     
     class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'owner',
        ]




class InterestsForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            'interests'
        ]

        widgets = {
            'interests': forms.CheckboxSelectMultiple()
        }
    



class MyLodgesForm(forms.ModelForm):

    class Meta:
        model = Lodge
        fields = [
            'title',
            'slug',
            'description',
            'province',
            'city',
            'address',
            'capacity',
            'price',
            'interests',
            'active',
        ]
        widgets = {
            'interests': forms.CheckboxSelectMultiple(),

            'province': forms.Select(attrs={'id': 'province'}),
            
            'city': forms.Select(attrs={'id': 'city'}),
        }


class LodgeImageForm(forms.ModelForm):
    class Meta:
        model = LodgeImage
        fields =[
            'image'
        ]
        widget = {
            'image' : forms.ImageField(),
        }


LodgeImageFormSet = inlineformset_factory(
    Lodge,
    LodgeImage,
    form=LodgeImageForm,
    extra=1,
    can_delete=True
)