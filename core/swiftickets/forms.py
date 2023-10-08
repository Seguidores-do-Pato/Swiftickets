from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Event, Purchase, Ticket

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['type', 'name', 'description','state', 'uf', 'open_at', 'close_at']

class PurchaseForm(ModelForm):
    total_price = forms.DecimalField(disabled=True, required=False)  # Campo para o preço total
    class Meta:
        model = Purchase
        fields = ['ticket', 'quantity', 'total_price']