from django.shortcuts import render
from vacuApp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django import forms
from .forms import UserLoginForm
# Create your views here.
from datetime import date

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
def register(response):
    return render(response,'register/register.html')


def home(response):
    return render(response,'home.html')

def infoPersonal(response,idu):
    o= User.objects
    usu=o.get(id=idu)
    edad = calculate_age(usu.birthDate)
    return render(response,'visualizarInfoPersonal.html', {"usuario":usu,"edad":edad})

def modificarInfo(response):
    return render(response,'modificarInfoPersonal.html')

def modContraseña(response):
    return render(response,'modificarContraseña.html')

def modMail(response):
    return render(response,'modificarMail.html')

def recuContraseña(response):
    return render(response,'recuperarContraseña.html')

def camContraseñaRecu(response):
    return render(response,'cambiarContraseñaRecuperada.html')

def registerCovid(response):
    return render(response,'register/registerCovid.html')

def registerGripe(response):
    return render(response,'register/registerGripe.html')

def registerFiebreA(response):
    return render(response,'register/registerFiebreA.html')

def registerCentro(response):
    return render(response,'register/registerCentro.html')

def login(response):
    return render(response,'login.html')

def login_view(request):
    login_form = UserLoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form.cleaned_data.get('mail')
        password = login_form.cleaned_data.get('password')
        token=login_form.cleaned_data.get('token')
        user = authenticate(request, email=email, password=password,token=token)
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesion correctamente')
            return redirect('visualizarInfoPersonal')
        else:
            messages.warning(
                request, 'Correo Electronico, Contraseña o Token invalida')
            return redirect('login')
    messages.error(request, 'Formulario Invalido')
    return redirect('login')     