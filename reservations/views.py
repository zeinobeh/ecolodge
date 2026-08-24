from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.views.generic import ListView
from .forms import ReservationForm
from .models import Reservation
from lodges.models import Lodge


# Create your views here.


def reservation_data(request, lodge_id):
    lodge = get_object_or_404(Lodge, id=lodge_id)
    if request.method == 'POST' :
        form = ReservationForm(request.POST)
        if form.is_valid() :
            with transaction.atomic():

                lodge = Lodge.objects.select_for_update().get(id=lodge_id)

                reservation = form.save(commit=False)
                reservation.user = request.user
                reservation.lodge = lodge

                reservation.check_data()
            
                reservation.total_price = lodge.price * (reservation.check_out - reservation.check_in).days

                conflict = Reservation.objects.filter(
                    lodge=lodge,
                    check_in__lt=reservation.check_out,
                    check_out__gt=reservation.check_in,
                    status=True,
                ).exists()

                if conflict:
                    return render(request, 'reserve.html', {
                        "message": "این اقامتگاه در این تاریخ رزرو شده است",
                        "form": form
                    })
                else:
                    reservation.status = True
                    reservation.save()
                
    else:
        form = ReservationForm()

    context = {
        "message": "صفحه رزرو",
        "form" : form
    }
    return render(request, 'reserve.html', context)




class ReservesView(ListView):
    model = Reservation
    template_name = "reserves_view.html"
    context_object_name = "reserves"
    paginate_by=10

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by('-id')
    


def cancel_reserve(request, reservation_id):
    reserve = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    reserve.status = False
    reserve.save()
    return redirect("reservations:reserves_view")


