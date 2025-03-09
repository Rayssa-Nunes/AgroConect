from django import forms
from django.forms import inlineformset_factory
from .models import Fair, FairDay, FairAddress


class FairAddressForm(forms.ModelForm):
    class Meta:
        model = FairAddress
        fields = ['address', 'district', 'city', 'state', 'cep', 'latitude', 'longitude']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control', 'id': 'address', 'required': True}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'id': 'district', 'required': True}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'id': 'state', 'required': True}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 8, 'id': 'cep', 'required': True}),
            # 'latitude': forms.TextInput(attrs={'class': 'form-control', 'id': 'latitude', 'required': False}),
            # 'longitude': forms.TextInput(attrs={'class': 'form-control', 'id': 'longitude', 'required': False}),
        }
        labels = {
            'address': 'Logradouro',
            'district': 'Bairro',
            'city': 'Cidade',
            'state': 'Estado',
            'cep': 'CEP',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
        }


class FairDayForm(forms.Form):
    DAYS_CHOICES = FairDay.DAYS_CHOICES

    day = forms.MultipleChoiceField(
        choices=DAYS_CHOICES, 
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    opening_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        required=False,
        initial='00:00:00'
    )
    closing_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        required=False,
        initial='00:00:00'
    )

    class Meta:
        model = FairDay
        fields = ['day', 'opening_time', 'closing_time']
