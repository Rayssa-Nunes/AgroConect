import re
import requests
from geopy import distance
from geopy.geocoders import Nominatim

from .models import FairAddress

class Location:
    # def __init__(self):
        # self.request = request

    
    def extract_coordinates(self, json):
        if 'location' in json and 'coordinates' in json['location']:
            coordinates = json['location']['coordinates']
            
            if 'latitude' in coordinates:
                json['latitude'] = coordinates['latitude']
            if 'longitude' in coordinates:
                json['longitude'] =  coordinates['longitude']
            
            del json['location']

        # print("Dados atualizados:", json)
        return json
    
    def get_coordinates(self, json):
        city, state = json.get('city'), json.get('state')

        geolocator = Nominatim(user_agent="app", timeout=5)

        location = geolocator.geocode(f"{city} - {state} - Brasil")
        # print(location.address)
        latitude, longitude = location.latitude, location.longitude
        json['latitude'] = str(latitude)
        json['longitude'] = str(longitude)
        # print(json)

        self.extract_coordinates(json)

        
    def verified_coordinates(self, json):
        location = json.get('location')
        if not location['coordinates']:
            # print(json.get('cep'))
            self.get_coordinates(json)
        else:
            self.extract_coordinates(json)
        return json

    
    def verified_cep(self, cep):
        regex_cep = r'^\d{5}-?\d{3}$' 
        cep = str(cep) 

        return re.sub(r'-', '', cep)  if re.match(regex_cep, cep) else None

    
    def get_location(self, cep=None):
        if cep:
            valid_cep = self.verified_cep(cep)
            # print(valid_cep)
            if valid_cep:
                BASE_URL = f'https://brasilapi.com.br/api/cep/v2/{cep}'
                
                try:
                    response = requests.get(BASE_URL, timeout=5)
                    if response.status_code == 200:
                        # print('resposta json', response.json())
                         return self.verified_coordinates(response.json())
                    else:
                        error_data = response.json()
                        print(error_data.get('message', 'Erro desconhecido'))
                except requests.exceptions.RequestException as e:
                    print('Erro na solicitação', e)
            else:
                print('Informe um cep válido, por favor!')
        else:
            print('Informe um cep, por favor!')


    def get_distinct_cep_locations(self):
        # locations = (
        #     FairAddress.objects
        #     .values('cep').distinct()
        #     .values('latitude', 'longitude', 'cep', 'city')
        # )
        locations = (
            FairAddress.objects
            .values('latitude', 'longitude', 'cep', 'city')
            .distinct()
        )
        return list(locations)
    

    def calculate_distance(self, coord, coords):
        distances = []

        for item in coords:
            if 'latitude' in item and 'longitude' in item:
                dist = distance.distance(
                    (float(coord['latitude']), float(coord['longitude'])),
                    (float(item['latitude']), float(item['longitude']))
                ).km
                distances.append({
                    item['cep']: dist
                })

        distances_sorted = sorted(distances, key=lambda x: list(x.values())[0])
        # print(distances_sorted)
        return distances_sorted[:5]
        