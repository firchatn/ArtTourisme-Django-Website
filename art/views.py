from django.shortcuts import render
from art.forms import RegisterForm, RegisterFormUpdate, AddAddress, LoginForm


def index(request):
    form = RegisterForm()
    form2 = LoginForm()

    return render(request, 'index.html', {'form': form, 'form2' : form2})
