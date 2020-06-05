from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from .models import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']

class OrderForm(ModelForm):
    class Meta:
        model = Order #defines the model we are using to build the form
        fields = '__all__' #creates a form with all the model entries from order


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User    #defines the model we are using to build the form
        fields = ['username', 'email', 'password1', 'password2'] #allowed fields