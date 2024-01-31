from django import forms

from .models import Allroducts


class ProductsForm(forms.ModelForm):
        class Meta:
                model = Allroducts
                fields = [
                    'Name',
                    'Image',
                    'Desc',
                    'Price',
                    'Container',
                    'Box',
                    'Percentage',
                    'Quantity',
                    'Date'
                ]

        