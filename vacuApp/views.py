from asyncio.windows_events import NULL
import smtplib
import random
from hashlib import scrypt
from subprocess import call
from unicodedata import name
from django.shortcuts import redirect, render
from requests import request
from vacuApp.models import *
from .admin import UserCreationForm
# Create your views here.
from django.http import HttpResponse
from pkg_resources import run_script
from vacuApp.models import User
from datetime import date
from django.dispatch import receiver
from .forms import RegisterCovid

EMAIL = 'vacunassist.contacto@gmail.com'
PASSW = 'xoejdavfzdfnoigf'
YO = 'agustinferrrr@gmail.com'                                              #Esto es para la prueba, despues se va
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    

        


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

def register(response):
        if(response.method == "POST"):
            form = UserCreationForm(response.POST)
            if form.is_valid():
                response.session["user_id"] = form.save().id   #Se crea el usuario aqui
                return redirect("/registerCovid")

            else:
                form = UserCreationForm()
                return render(response,'register/register.html',{"form":form})
        else:
            form = UserCreationForm()
            return render(response,'register/register.html',{"form":form})


def registerCovid(response):
    form = RegisterCovid()
    if(response.method == "POST"):
            form = RegisterCovid(response.POST)
            if form.is_valid():
                data = form.cleaned_data
                response.session["covid"] = data["covid"]
                if (data["covid_date"]):
                    response.session["covid_date"] = str(data["covid_date"])
                print(response.session["covid"])
                return redirect("/registerGripe")

            else:
                form = RegisterCovid()
                return render(response,'register/registerCovid.html',{"form":form})
    else:
        form = RegisterCovid()
        return render(response,'register/registerCovid.html',{"form":form})

    

def registerGripe(response):
    return render(response,'register/registerGripe.html')

def registerFiebreA(response):
    return render(response,'register/registerFiebreA.html')

def registerCentro(response):
    return render(response,'register/registerCentro.html')

def login(response):
    return render(response,'login.html')

def enviaremail(response): 
    
    #user = request.session["user"]
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:                       #Esto prepara la conexion con gmail, utilizando el puerto 587, y lo llamamos smtp   
        user = User.objects.get(id=response.session["user_id"]) 
        smtp.ehlo()                                                         #Nos identifica con gmail
        smtp.starttls()                                                     #Encripta algo que no se como se llama
        smtp.ehlo()                                                         #Nos identificamos de nuevo porque nos encriptamos    
        smtp.login(EMAIL, PASSW)                                            #Nos logeamos (xoejdavfzdfnoigf)
        TOKEN = random.randint(1000, 9999)
        user.token = TOKEN
        user.save()
        subject = 'Confirmacion de cuenta'                                  #Asunto del email
        body = 'Este es un mensage autogenerado por VacunAssist, tu TOKEN de ingreso es ' + str(TOKEN)          #Cuerpo del email

        msg = f'Subject: {subject}\n\n{body}'                               #Es necesario formatear el mensaje (f) para que lo tome gmail

        smtp.sendmail(EMAIL, user.email, msg)                                       #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion

          
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


## User(name=data["name"] data,center = None, 
                ##token = None, password = data["password"],
                ##sex = data, birthDate = data,
                ##DNI = data, email = data,
                ##surname =data )