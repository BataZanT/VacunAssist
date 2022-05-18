import smtplib
import random
from hashlib import scrypt
from subprocess import call
from django.shortcuts import render
from vacuApp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django import forms
from .forms import UserLoginForm
from .forms import Register
# Create your views here.
from django.http import HttpResponse
from pkg_resources import run_script
from vacuApp.models import *
from datetime import date
from django.dispatch import receiver

EMAIL = 'vacunassist.contacto@gmail.com'
PASSW = 'xoejdavfzdfnoigf'
YO = 'agustinferrrr@gmail.com'                                              #Esto es para la prueba, despues se va

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
def register(response):
    form = Register()
    return render(response,'register/register.html',{"form":form})


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
def enviaremail(request): 
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:                       #Esto prepara la conexion con gmail, utilizando el puerto 587, y lo llamamos smtp
        smtp.ehlo()                                                         #Nos identifica con gmail
        smtp.starttls()                                                     #Encripta algo que no se como se llama
        smtp.ehlo()                                                         #Nos identificamos de nuevo porque nos encriptamos    
        smtp.login(EMAIL, PASSW)                                            #Nos logeamos (xoejdavfzdfnoigf)
        TOKEN = random.randint(1000, 9999)
        subject = 'Confirmacion de cuenta'                                  #Asunto del email
        body = 'Este es un mensage autogenerado por VacunAssist, tu TOKEN de ingreso es ' + str(TOKEN)          #Cuerpo del email

        msg = f'Subject: {subject}\n\n{body}'                               #Es necesario formatear el mensaje (f) para que lo tome gmail

        smtp.sendmail(EMAIL, YO, msg)                                       #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion

 
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
