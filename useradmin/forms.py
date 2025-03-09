from django import forms

from core.models import Product

class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category', 'name', 'image', 'description',
            'price', 'old_price', 'specifications', 'type', 'stock_count',
            'life', 'product_status', 'in_stock'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'specifications': forms.Textarea(attrs={'rows': 3}),
        }
