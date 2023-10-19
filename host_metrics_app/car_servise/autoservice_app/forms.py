from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


from .models import Service, Order, Basket

User = get_user_model()


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
            }
        )
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_nickname', 'price']


class BasketForm(forms.ModelForm):
    class Meta:
        model = Basket
        fields = ['user', 'number_of_services', 'services']