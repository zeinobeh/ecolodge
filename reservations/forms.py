from django import forms
from django.contrib.auth import get_user_model
from .models import Reservation


#


class ReservationForm(forms.ModelForm):
    
    class Meta:
        model = Reservation
        fields = [
            'check_in',
            'check_out',
            'guest_count',
        ]

        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }


