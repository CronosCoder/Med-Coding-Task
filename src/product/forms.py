
from django import forms
from product.models import Variant,Product

class VariantForm(forms.ModelForm):
    class Meta:
        model = Variant
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'active'})
        }

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'sku', 'description']

    def save(self, commit=True):
        product = super().save(commit)
        return product