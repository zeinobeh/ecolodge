from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.views.generic import ListView
from .forms import ReservationForm
from .models import Reservation
from lodges.models import Lodge
from django.contrib import messages

from datetime import date
import jdatetime

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

                if reservation.check_in > reservation.check_out or date.today() > reservation.check_in :
                    messages.error(request, "تاریخ را درست وارد کنید")
                    return redirect('lodges:lodge_detail', slug=lodge.slug) 

                if reservation.guest_count > reservation.lodge.capacity :
                    messages.error(request, "تعداد مهمان از ظرفیت اقامتگاه بیشتر است")
                    return redirect('lodges:lodge_detail', slug=lodge.slug)
                
                reservation.total_price = lodge.price * (reservation.check_out - reservation.check_in).days

                conflict = Reservation.objects.filter(
                    lodge=lodge,
                    check_in__lt=reservation.check_out,
                    check_out__gt=reservation.check_in,
                    status=True,
                ).exists()

                if conflict:
                    messages.error(request, "این اقامتگاه در این تاریخ رزرو شده است")
                    return redirect('lodges:lodge_detail', slug=lodge.slug)
                else:
                    reservation.status = True
                    reservation.save()
                    messages.success(request, "با موفقیت رزرو شد.")
                    return redirect('lodges:lodge_detail', slug=lodge.slug)
        else:
            print("FORM IS INVALID")
            print(form.errors)        
    else:
        form = ReservationForm()

    context = {
        "lodge" : lodge ,
        "form" : form
    }
    return render(request, 'lodge_detail.html', context)




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


