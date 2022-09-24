from django.forms import ModelForm, fields
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order

class OrderForm (ModelForm):
    class Meta:
        model = Order
        fields = '__all__'      # if we wanted just some fields, we would have given a list. e.g. fields = ['customer', 'status']

class CreateUserForm (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']