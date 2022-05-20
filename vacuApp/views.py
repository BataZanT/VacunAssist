from email import message
import smtplib
import random
from hashlib import scrypt
from subprocess import call
from django.shortcuts import render
from django.http import HttpResponse
from vacuApp.models import *
from django.contrib import messages
from django.http.response import HttpResponse
from django.http import HttpResponse
from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from .admin import UserCreationForm
from datetime import date
from .forms import RegisterCovid,RegisterGripe,RegisterFiebreA,RegisterCentro
from . import validators
from django.contrib.auth.hashers import check_password


EMAIL = 'vacunassist.contacto@gmail.com'
PASSW = 'xoejdavfzdfnoigf'
YO = 'agustinferrrr@gmail.com'                                              #Esto es para la prueba, despues se va


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))




def home(response):
    return render(response,'home.html')

def infoPersonal(response):
    o= User.objects.all()
    idu=response.session["user_id"]
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
            mail = response.POST['email']
            DNI= response.POST['DNI']
            form.is_valid()
            data = form.cleaned_data
            data["DNI"] = DNI
            data["email"] = mail
            message = validators.validarRegister(data)
            if message == '':
                user = form.save()
                response.session["reg_user_id"] = user.id
                return redirect("/registerCovid")

            else:
                messages.warning(response, message)
                return render(response,'register/register.html',{"form":form})
        else:
            form = UserCreationForm()
            return render(response,'register/register.html',{"form":form})

def registerCovid(response):
    form = RegisterCovid()
    if(response.method == "POST"):

            form = RegisterCovid(response.POST)
            form.is_valid()
            data = form.cleaned_data
            message = validators.validarCovid(data)
            print(message)
            if message == '':
                response.session["covid"] = data["covid"]
                if (data["covid_date"]):
                    response.session["covid_date"] = str(data["covid_date"])
                return redirect("/registerGripe")

            else:
                messages.warning(response, message)
                return render(response,'register/registerCovid.html',{"form":form})
    else:
        form = RegisterCovid()
        return render(response,'register/registerCovid.html',{"form":form})

    

def registerGripe(response):
    form = RegisterGripe()
    if(response.method == "POST"):
            form = RegisterGripe(response.POST)
            form.is_valid()
            data = form.cleaned_data
            message = validators.validarGripe(data)
            if message == '' :
                response.session["gripe"] = data["gripe"]
                if (data["gripe_date"]):
                    response.session["gripe_date"] = str(data["gripe_date"])
                return redirect("/registerFiebreA")

            else:
                messages.warning(response, message)
                return render(response,'register/registerGripe.html',{"form":form})
    else:
        form = RegisterGripe()
        return render(response,'register/registerGripe.html',{"form":form})

def registerFiebreA(response):
    form = RegisterFiebreA()
    if(response.method == "POST"):
            form = RegisterFiebreA(response.POST)
            form.is_valid()
            data = form.cleaned_data
            message = validators.validarFiebreA(data)
            if message == '':
                response.session["fiebreA"] = data["fiebreA"]
                if (data["fiebreA_date"]):
                    response.session["fiebreA_date"] = str(data["fiebreA_date"])
                return redirect("/registerCentro")

            else:
                messages.warning(response,message)
                return render(response,'register/registerfiebreA.html',{"form":form})
    else:
        form = RegisterFiebreA()
        return render(response,'register/registerfiebreA.html',{"form":form})

def registerCentro(response):
    form = RegisterCentro()
    if(response.method == "POST"):
            form = RegisterCentro(response.POST)
            if form.is_valid():
                data = form.cleaned_data
                response.session["center"] = data["center"]
                completarUsuario(response)
                return enviaremail(response)

            else:
                form = RegisterCentro()
                return render(response,'register/registerCentro.html',{"form":form})
    else:
        form = RegisterCentro()
        return render(response,'register/registerCentro.html',{"form":form})

def login(response):
    return render(response,'login.html')


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
                            auth.login(response,usu)
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
 

def enviaremail(response): 
    
    #user = request.session["user"]
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:                               #Esto prepara la conexion con gmail, utilizando el puerto 587, y lo llamamos smtp 
        user = User.objects.get(id=response.session["reg_user_id"]) 
        NAME = user.name
        SURNAME =  user.surname
        TOKEN = user.token
        NCOMPLETO = str(NAME) + ' ' + str(SURNAME)
        DESTINATARIO = user.email
        user.save()

        smtp.ehlo()                                                                 #Nos identifica con gmail
        smtp.starttls()                                                             #Encripta algo que no se como se llama
        smtp.ehlo()                                                                 #Nos identificamos de nuevo porque nos encriptamos    
        smtp.login(EMAIL, PASSW)                                                    #Nos logeamos (xoejdavfzdfnoigf)
        TOKEN = random.randint(1000, 9999)

        subject = 'Confirmacion de cuenta'                                          #Asunto del email
        body = 'Este es un mensage autogenerado por VacunAssist. Para acceder a su cuenta su TOKEN es ' + str(TOKEN)          
        msg = f'Subject: {subject}\n\n{body}'                                       #Es necesario formatear el mensaje (f) para que lo tome gmail

        smtp.sendmail(EMAIL, DESTINATARIO, msg)                                       #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion


    response.session.flush()
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")


## User(name=data["name"] data,center = None, 
                ##token = None, password = data["password"],
                ##sex = data, birthDate = data,
                ##DNI = data, email = data,
                ##surname =data
                ##surname =data

def completarUsuario(response):
    u = User.objects.get(id=response.session["reg_user_id"])
    c = Center.objects.get(id=response.session["center"])
    u.center = c
    h = History(covid_doses = response.session["covid"],gripe = response.session["gripe"],fiebreA = response.session["fiebreA"],fiebreA_eleccion = False,user = u)
    if (int(response.session["covid"]) > 0):
        h.covid_date = response.session["covid_date"]
    if (int(response.session["gripe"]) == 1):
        h.gripe_date = response.session["gripe_date"]
    if (int(response.session["fiebreA"]) == 1):
        h.fiebreA_date = response.session["fiebreA_date"]
    u.save()
    h.save()
    asignarVacunas(u)
    return str(u.history)


def asignarVacunas(user):
    if (user.history.covid < 2):
        vac = Vaccine.objects.get(name="covid")
        turnoC = Appointment(state=0,center=user.center,vaccine=vac,patient=user)
        turnoC.save()
    if (user.history.gripe == False):
        vac = Vaccine.objects.get(name="gripe")
        turnoG = Appointment(state=0,center=user.center,vaccine=vac,patient=user)
        turnoG.save()
    if (user.history.fiebreA == False):
        if (calculate_age(user.birthDate) < 60):
            vac = Vaccine.objects.get(name="fiebreA")
            turnoF = Appointment(state=0,center=user.center,vaccine=vac,patient=user)
            turnoF.save()
    
def visualizar(response):
    return render(response,'visualizarInfoPersonal.html')
