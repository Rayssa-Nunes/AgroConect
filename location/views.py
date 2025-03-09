from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Fair, FairDay
from .forms import FairDayForm, FairAddressForm

from geopy.geocoders import Nominatim

@login_required
def fair_view(request):
    if request.method == "POST":
        print(request.POST)
        print(request.POST.get('latitude'))
        print(request.POST.get('longitude'))
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        form_address = FairAddressForm(request.POST)
        form_day = FairDayForm(request.POST)

        if form_address.is_valid() and form_day.is_valid():
            if not latitude and not longitude:
                geolocator = Nominatim(user_agent="app", timeout=5)
                location = geolocator.geocode(f"{request.POST.get('city')} - {request.POST.get('state')} - Brasil")
                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                    print(latitude, longitude)

            address = form_address.save(commit=False)
            address.latitude = latitude
            address.longitude = longitude
            address.save()
   
            fair = Fair.objects.create(address=address)
            fair.users.add(request.user)

            for day in form_day.cleaned_data['day']:
                opening_time = request.POST.get(f'opening_time_{day}')
                closing_time = request.POST.get(f'closing_time_{day}')

                print(opening_time, closing_time)

                FairDay.objects.create(
                    fair=fair,
                    day=day,
                    opening_time=opening_time,
                    closing_time=closing_time
                )

            messages.success(request, 'Feira cadastrada com sucesso!')
            return redirect('fair')

    else:
        form_address = FairAddressForm()
        form_day = FairDayForm()
    
    return render(request, 'location/fair.html', {
        'form_address': form_address,
        'form_day': form_day
    })


@login_required
def fair_list(request):
    user = request.user
    user_fairs = user.fairs.all()

    return render(request, 'location/user_fairs.html', {'user_fairs': user_fairs})


@login_required
def leave_fair(request, id):
    fair = get_object_or_404(Fair, id=id)

    if request.user in fair.users.all():
        fair.users.remove(request.user)

        if not fair.users.exists():
            address = fair.address
            fair.delete()

            if address and not Fair.objects.filter(address=address).exists():
                address.delete()

        messages.success(request, "Você saiu da feira com sucesso!")

    else:
        messages.error(request, "Você não está registrado nesta feira.")

    return redirect('fair_list')

