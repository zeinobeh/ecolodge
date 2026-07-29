from django import forms
from django.contrib.auth import get_user_model

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(attrs={'maxlength':'150'})
    )
    password = forms.CharField(
        widget= forms.PasswordInput()
    )


User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(attrs={'maxlength':'150'})
    )
    email = forms.EmailField(
        widget = forms.EmailInput()
    )
    password = forms.CharField(
        widget= forms.PasswordInput()
    )
    password2 = forms.CharField(
        label= 'confirm password',
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
            raise forms.ValidationError('Try another username')
        return username 

    def clean_email(self):
        email=self.cleaned_data.get('email')
        query=User.objects.filter(email=email)   
        if query.exists():
            raise forms.ValidationError('Try another email')
        return email