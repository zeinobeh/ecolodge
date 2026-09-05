from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):

    check_in = forms.DateField(
        input_formats=['%Y/%m/%d']
    )

    check_out = forms.DateField(
        input_formats=['%Y/%m/%d']
    )

    class Meta:
        model = Reservation
        fields = ['guest_count', 'check_in', 'check_out']