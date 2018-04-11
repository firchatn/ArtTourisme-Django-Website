# coding=utf-8
from art.models import *
from django import forms
from django.forms import ModelForm


class RegisterForm(ModelForm):
    first_name = forms.CharField(label='Votre prénom', required=True)
    last_name = forms.CharField(label='Votre nom', required=True)
    email = forms.EmailField(label='Votre adresse e-mail', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


class RegisterFormUpdate(ModelForm):
    first_name = forms.CharField(label='Votre prénom', required=True)
    last_name = forms.CharField(label='Votre nom', required=True)
    email = forms.EmailField(label='Votre adresse e-mail', required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AddAddress(ModelForm):
    class Meta:
        model = Address
        fields = ['gender', 'first_name', 'last_name', 'company', 'address', 'additional_address',
                  'postcode', 'city', 'phone', 'mobilephone', 'fax', 'workphone']
