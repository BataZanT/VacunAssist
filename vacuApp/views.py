from email import message
import smtplib
import random
from hashlib import scrypt
from subprocess import call
from unicodedata import name
from django.shortcuts import render
from django.http import HttpResponse
from vacuApp.models import *
from django.contrib import messages
from django.http.response import HttpResponse
from django.http import HttpResponse
from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from .admin import UserCreationForm
from datetime import date, datetime
from .forms import RegisterCovid,RegisterGripe,RegisterFiebreA,RegisterCentro
from . import validators
from django.contrib.auth.hashers import check_password

EMAIL = 'vacunassist.contacto@gmail.com'
PASSW = 'xoejdavfzdfnoigf'

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
    idu=response.session['user_id']
    o=User.objects.all()
    usu=o.get(id=idu)
    return render(response,'modificarInfoPersonal.html',{"usuario":usu})

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
        
def CerrarSesion(response):
    response.session.flush()
    return redirect('http://127.0.0.1:8000/')

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
                    if (usu.token == token):
                            response.session["user_id"] = usu.id
                            return redirect('/homeUsuario')                           
                    else:
                        messages.error(response, 'Token invalido')
                else:
                    messages.error(response, ' Contraseña invalida')
            else: 
                messages.error(response, ' Mail invalido')
        else:
            messages.error(response, 'No hay usuarios cargados en la base')
        return redirect('http://127.0.0.1:8000/login')     

def enviaremail(response): 
    
    #user = request.session["user"]
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:                               #Esto prepara la conexion con gmail, utilizando el puerto 587, y lo llamamos smtp 
        user = User.objects.get(id=response.session["reg_user_id"]) 
        NAME = user.name
        SURNAME =  user.surname
        NCOMPLETO = str(NAME) + ' ' + str(SURNAME)
        DESTINATARIO = user.email
        user.save()

        smtp.ehlo()                                                                 #Nos identifica con gmail
        smtp.starttls()                                                             #Encripta algo que no se como se llama
        smtp.ehlo()                                                                 #Nos identificamos de nuevo porque nos encriptamos    
        smtp.login(EMAIL, PASSW)                                                    #Nos logeamos (xoejdavfzdfnoigf)
        TOKEN = random.randint(1000, 9999)
        user.token = TOKEN
        user.save()

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
    if (calculate_age(user.birthDate) > 18) and (int(user.history.covid_doses) < 2):
        vacC = Vaccine.objects.get(name="Covid")
        user.appointment_set.create(state=0,center=user.center,vaccine=vacC)

    if (user.history.gripe == '0'):
        vacG = Vaccine.objects.get(name="Gripe")
        user.appointment_set.create(state=0,center=user.center,vaccine=vacG)
    elif (calculate_age(datetime.strptime(user.history.gripe_date, '%Y-%m-%d').date()) > 0):
        vacG = Vaccine.objects.get(name="Gripe")
        user.appointment_set.create(state=0,center=user.center,vaccine=vacG)
    
def visualizar(response):
    return render(response,'visualizarInfoPersonal.html')

def CerrarSesion(response):
    response.session.flush()
    return redirect('http://127.0.0.1:8000/')

def homeUsuario(response):
    o= User.objects.all()
    idu=response.session["user_id"]
    usu=o.get(id=idu)
    NCOMPLETO = usu.name + ' ' + usu.surname
    turnos = usu.appointment_set.all()
    fiebre_disp = False
    vacF = Vaccine.objects.get(name="Fiebre Amarilla")
    if ((usu.history.fiebreA == False)) and (calculate_age(usu.birthDate) < 60):
        if( not tieneTurno(usu,vacF)):
            fiebre_disp = True            
    return render(response,'inicioPaciente.html', {'NOMBRE': NCOMPLETO, 'turnos': turnos, 'fiebre_disp':fiebre_disp,'sexo':usu.sex})
   
def modificarContraseña(response):
    ca=response.POST["contActual"]
    idu=response.session["user_id"]
    o=User.objects.all()
    user=o.get(id=idu)
    if check_password(ca, user.password):
        cn=response.POST["contNueva"]
        upper = False
        for character in cn:
            if character.isupper():
                    upper = True
        if(not upper):
            messages.warning(response, 'La contraseña nueva debe contener al menos una letra mayuscula')
        elif ca==cn:
            messages.warning(response, 'La contraseña actual y la contraseña nueva son iguales')
        else:
            cnr=response.POST["contNuevaR"]
            if (not cn== cnr):
                messages.warning(response, 'Las contraseñas no coinciden')
            else:
                user.set_password(cn)
                user.save()
                messages.warning(response, 'Las contraseñas se ha modificado correctamente')
                return redirect('http://127.0.0.1:8000/modificarInfo') 
    else:
        messages.warning(response, 'La contraseña actual no es correcta.')
    return redirect('http://127.0.0.1:8000/modContraseña') 
 
def asignarTurnoFiebreA(response):
    o= User.objects.all()
    idu=response.session["user_id"]
    usu=o.get(id=idu)
    vacF = Vaccine.objects.get(name="Fiebre Amarilla")
    turnoF = Appointment(state=0,center=usu.center,vaccine=vacF,patient=usu)
    turnoF.save()
    return redirect('/homeUsuario')

def tieneTurno(user,vacuna):  # se puede usar con cualquier vacuna, el segundo parametro tiene que ser el objeto de la vacuna
    tiene = False
    for turno in user.appointment_set.all():
        if turno.vaccine == vacuna:
            tiene = True
    return tiene
    NOMBRE = usu.name
    APELLIDO = usu.surname
    NCOMPLETO = NOMBRE + ' ' + APELLIDO
    return render(response,'inicioPaciente.html', {'NOMBRE': NCOMPLETO})

def validarCambioMail(response):
        mailN = response.POST['mailNuevo']
        mailNRepetido = response.POST['mailNuevoRepetido']

        o= User.objects.all()
        if o!=None:
            idUsuario = response.session["user_id"]
            usu = o.get(id = idUsuario)
            if (usu.email != mailN):
                usuCopiado = o.filter(email = mailN)    
                if usuCopiado:
                    messages.warning(response, 'El email ingresado ya pertenece a otra cuenta registrada en el sistema')
                else: 
                    if (mailN == mailNRepetido):
                        usu.email = mailN
                        usu.save() 
                        messages.success(response, "Informacion actualizada con exito" )                 
                        return redirect('http://127.0.0.1:8000/infoPersonal') 
                    else:
                        messages.error(response, 'Los mails no coinciden')
            else:  
                messages.error(response, 'El mail nuevo no puede ser el actual')
        else:
            messages.error(response, 'No hay usuarios cargados en la base')  
        return redirect('http://127.0.0.1:8000/modMail')

def modCentro(response):
    o= User.objects.all()
    idu=response.session["user_id"]
    usu=o.get(id=idu)
    CENTRO = usu.center
    return render(response,'modificarCentro.html', {'centroActual': CENTRO})

def validarCambioCentro(response):
    c = Center.objects.get(id = response.POST.get('elegido'))
    o= User.objects.all()
    if o!=None:
        idUsuario = response.session['user_id']
        usu = o.get(id = idUsuario)
        if (usu.center != c):
            usu.center = c
            usu.save() 
            messages.success(response, "Informacion actualizada con exito" )                 
            return redirect('/infoPersonal')
        else: 
            messages.error(response, 'El centro elegido no puede ser el actual')
            return redirect('/modCentro')               
    else:
        messages.error(response, 'No hay usuarios cargados en la base')  
    return redirect('/modCentro')

def borrarRegistro(response):
    o= User.objects.all()
    if o!=None:
        print (response.session['reg_user_id'])
        idUsuario = response.session['reg_user_id']
        usu = o.get(id = idUsuario)
        usu.delete() 
        messages.info(response, "Se ha cancelado el registro" )                 
        return redirect('/')              
    else:
        messages.error(response, 'No hay usuarios cargados en la base')  
    return redirect('/')