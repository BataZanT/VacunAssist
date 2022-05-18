import email
import smtplib
import random
from django.shortcuts import render, redirect
from vacuApp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
from .forms import Register
# Create your views here.
from django.http import HttpResponse
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
    
from .forms import UserForm

def validar(request):
        mail=request.POST['mail']
        contraseña=request.POST['contraseña']
        token=request.POST['token']
        o= User.objects
        usu=o.get(email=mail)
        if usu!=None:
            if usu.password==contraseña:
                if usu.token==token:
                    login_form = UserForm(request.POST)
                    if login_form.is_valid():
                        username= login_form.cleaned_data.get('username')
                        password = login_form.cleaned_data.get('password')
                        auth_user = authenticate(request, username=username, password=password)
                        login(auth_user) 
                        messages.success(request, 'Has iniciado sesion correctamente') 
                        return redirect('vinfoPersonal/',usu.Id)
                    else:   
                        messages.warning(request, 'Ocurrio un problema')
                else:
                    messages.warning(request, 'Token invalido')
            else:
                messages.warning(request, ' Contraseña invalido')
        else: 
            messages.warning(request, ' Mail invalido')
        return redirect('http://127.0.0.1:8000/login')    


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
