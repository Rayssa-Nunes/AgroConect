from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from geopy.geocoders import Nominatim
import folium

from .models import Fair, FairDay, FairAddress
from .forms import FairDayForm, FairAddressForm
from .location import Location


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



coordinates = [
    {'gramado': {'latitude': '-29.386051225274144', 'longitude': '-50.89690380192829'}},
    {'arara': {'latitude': '-6.845475646209959', 'longitude': '-35.7725301195203'}},
    {'bananeiras': {'latitude': '-6.7537682', 'longitude': '-35.6338343'}},
    {'solanea': {'latitude': '-6.7540351', 'longitude': '-35.6621943'}}
]


# def map_view(request):
#     loc = Location()
#     coords = loc.get_distinct_cep_locations()

#     mapa = folium.Map(location=[coords[0]['latitude'], coords[0]['longitude']], zoom_start=7)

#     if request.method == 'POST':
#         cep = request.POST.get('cep')
#         if cep:
#             coord = loc.get_location(cep)

#             if coord:
#                 distances = loc.calculate_distance(coord, coords)
#                 location = (float(coord['latitude']), float(coord['longitude']))
#                 mapa = folium.Map(location=location)

#                 folium.Marker(location=location, popup=coord['city'], icon=folium.Icon(color='red')).add_to(mapa)
                
#                 for dist in distances:
#                     for cep, distance_value in dist.items():
#                         cep_coords = next((item for item in coords if item['cep'] == cep), None)
#                         if cep_coords:
#                             cep_location = (float(cep_coords['latitude']), float(cep_coords['longitude']))
#                             folium.Marker(location=cep_location, popup=f'{cep}: {distance_value:.2f} km').add_to(mapa)

#                 ceps = [item['cep'] for item in coords]
#                 fairs = Fair.objects.filter(address__cep__in=ceps)
#     else:
    
#         for location in coords:
#             folium.Marker(
#                 location=[location['latitude'], location['longitude']],
#                 popup=f"Cidade: {location['city']}, CEP: {location['cep']}"
#             ).add_to(mapa)

#     mapa_html = mapa._repr_html_()

#     context = {
#         'locations': coords,
#         'mapa_html': mapa_html,
#         'fairs': fairs if request.method == 'POST' and cep else None,
#     }
#     return render(request, 'location/map.html', context)

def map_view(request):
    loc = Location()
    coords = loc.get_distinct_cep_locations()

    mapa_html = None
    distances = None
    fairs = None

    cep = request.GET.get('cep')
    if cep:
        coord = loc.get_location(cep)
        if coord:
            distances = loc.calculate_distance(coord, coords)
            location = (float(coord['latitude']), float(coord['longitude']))
            mapa = folium.Map(location=location)

            folium.Marker(location=location, popup=coord['city'], icon=folium.Icon(color='red')).add_to(mapa)
            
            for dist in distances:
                for cep, distance_value in dist.items():
                    cep_coords = next((item for item in coords if item['cep'] == cep), None)
                    if cep_coords:
                        cep_location = (float(cep_coords['latitude']), float(cep_coords['longitude']))
                        folium.Marker(location=cep_location, popup=f'{cep}: {distance_value:.2f} km').add_to(mapa)

            ceps = [item['cep'] for item in coords]
            fairs = Fair.objects.filter(address__cep__in=ceps)
            mapa_html = mapa._repr_html_()
    else:
        mapa = folium.Map(location=[coords[0]['latitude'], coords[0]['longitude']], zoom_start=7)
        for location in coords:
            folium.Marker(
                location=[location['latitude'], location['longitude']],
                popup=f"Cidade: {location['city']}, CEP: {location['cep']}"
            ).add_to(mapa)

        mapa_html = mapa._repr_html_()

    context = {
        'locations': coords,
        'mapa_html': mapa_html,
        'fairs': fairs,
        'distances': distances,
    }
    return render(request, 'location/map.html', context)
