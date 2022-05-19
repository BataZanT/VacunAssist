import email
import smtplib
import random
from urllib import response
from django.shortcuts import render, redirect
from vacuApp.models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse
# Create your views here.
from django.http import HttpResponse
from vacuApp.models import *
from asyncio.windows_events import NULL
import smtplib
import random
from hashlib import scrypt
from subprocess import call
from unicodedata import name
from django.shortcuts import render
from vacuApp.models import *
from .admin import UserCreationForm
# Create your views here.
from django.http import HttpResponse
from pkg_resources import run_script
from vacuApp.models import User
from datetime import date
from django.dispatch import receiver

EMAIL = 'vacunassist.contacto@gmail.com'
PASSW = 'xoejdavfzdfnoigf'
YO = 'agustinferrrr@gmail.com'                                              #Esto es para la prueba, despues se va
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    
def register(response):
        if(response.method == "POST"):
            form = UserCreationForm(response.POST)
            if form.is_valid():
                data = form.cleaned_data
                form.save()
                print(User.objects.all())
                user = User( name = data["name"] ,center = None, token = None, password = data["password1"],sex = data["sex"], birthDate = data["birthDate"],DNI = str(data["DNI"]), email = data["email"],surname = data["surname"] )
                return render(response,'home.html')
                return enviaremail(user)
            else:
                form = UserCreationForm()
                print('ourrio un error')
                return render(response,'register/register.html',{"form":form})
        else:
            form = UserCreationForm()
            return render(response,'register/register.html',{"form":form})


def home(response):
    return render(response,'home.html')

def infoPersonal(response):
    o= User.objects.all()
    idu=response.session["user_id"]
    messages.success(response, 'Has iniciado sesion correctamente')
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
     return enviaremail()
     return render(response,'register/registerCovid.html')

    

def registerGripe(response):
    return render(response,'register/registerGripe.html')

def registerFiebreA(response):
    return render(response,'register/registerFiebreA.html')

def registerCentro(response):
    return render(response,'register/registerCentro.html')

def login(response):
    return render(response,'login.html')
    
from django.contrib.auth.hashers import check_password
def validar(response):
        mail=response.POST['mail']
        contraseña=response.POST['contraseña']
        token=response.POST['token']
        o= User.objects.all()
        if o!=None:
            usu=o.filter(email=mail)
            if usu:
                usu=o.get(email=mail)
                if check_password(contraseña, usu.password):
                    if usu.token==token:
                            response.session["user_id"]=usu.id
                            return redirect('/infoPersonal')
                    else:
                        messages.warning(response, 'Token invalido')
                else:
                    messages.warning(response, ' Contraseña invalido')
            else: 
                messages.warning(response, ' Mail invalido')
        else:
            messages.warning(response, 'No hay usuarios cargdos en la base')
        return redirect('http://127.0.0.1:8000/login')    
 

def enviaremail(user): 
    
    #user = request.session["user"]
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:                       #Esto prepara la conexion con gmail, utilizando el puerto 587, y lo llamamos smtp   
        smtp.ehlo()                                                         #Nos identifica con gmail
        smtp.starttls()                                                     #Encripta algo que no se como se llama
        smtp.ehlo()                                                         #Nos identificamos de nuevo porque nos encriptamos    
        smtp.login(EMAIL, PASSW)                                            #Nos logeamos (xoejdavfzdfnoigf)
        TOKEN = random.randint(1000, 9999)
        subject = 'Confirmacion de cuenta'                                  #Asunto del email
        body = 'Este es un mensage autogenerado por VacunAssist, tu TOKEN de ingreso es ' + str(TOKEN)          #Cuerpo del email

        msg = f'Subject: {subject}\n\n{body}'                               #Es necesario formatear el mensaje (f) para que lo tome gmail
        smtp.sendmail(EMAIL, user.email, msg)                                       #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion

          
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


## User(name=data["name"] data,center = None, 
                ##token = None, password = data["password"],
                ##sex = data, birthDate = data,
                ##DNI = data, email = data,
                ##surname =data

from .forms import UserLoginForm
def validar2(request): #no se esta usandp
    if(request.method == "POST"):
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            email= login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            token=login_form.cleaned_data.get('token')
            auth_user = authenticate(request, email=email, password=password, token=token)
            if auth_user is not None:
                login(request,auth_user) 
                messages.success(request, 'Has iniciado sesion correctamente') 
                return redirect('vinfoPersonal/1')
            else:   
                messages.warning(request, 'Ocurrio un problema')
        else:
            messages.warning(request, 'problema')
    return redirect('http://127.0.0.1:8000/login') 