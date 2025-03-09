from .models import *
from django import forms
from django.contrib.admin import widgets

# Форма для создания заказа
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["table_number"]

    table_number = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={'class': 'table_field', 'placeholder': 'Номер стола'}))