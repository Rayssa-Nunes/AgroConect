from django import forms

from .models import Vendor, Address

class VendorDetailsForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['cnpj', 'legal_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cnpj'].widget.attrs.update({'class': 'form-control', 'placeholder': 'CNPJ', 'required': True})
        self.fields['cnpj'].label = ''

        self.fields['legal_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Razão social', 'required': True})
        self.fields['legal_name'].label = ''


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['cep', 'address', 'number', 'district', 'city', 'state']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Logradouro', 'id': 'address', 'required': True})
        self.fields['district'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Bairro', 'id': 'district',  'required': True})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Cidade', 'id': 'city', 'required': True})
        self.fields['number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Número', 'id': 'number',})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'placeholder': 'UF', 'id': 'state', 'required': True})
        self.fields['cep'].widget.attrs.update({'class': 'form-control', 'placeholder': 'CEP', 'id': 'cep', 'required': True})


    # def save(self, *args, **kwargs):
    #     if hasattr(self.user, 'vendor'):
    #         self.status = True
    #     super().save(*args, **kwargs)


