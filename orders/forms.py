from django import forms
from .models import Order
from shops.models import Product

class OrderForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=Product.objects.filter(available=True))

    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'address', 'product', 'quantity', 'comment']
