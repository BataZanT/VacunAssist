from ctypes.wintypes import USHORT
from select import select
import smtplib
import random
from sqlite3 import Date
from xml.dom.minidom import TypeInfo
from django.shortcuts import render
from .models import *
from django.contrib import messages
from django.http.response import HttpResponse
from django.http import HttpResponse
from asyncio.windows_events import NULL
from django.shortcuts import redirect, render
from .admin import UserCreationForm
from datetime import date, datetime
from .forms import Observaciones, RegisterCovid,RegisterGripe,RegisterFiebreA,RegisterCentro
from . import validators
from django.contrib.auth.hashers import check_password
# importing the necessary libraries
from django.views.generic import View
from .process import html_to_pdf
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from tkinter import *
from tkinter import messagebox
from datetime import timedelta

EMAIL = 'vacunassist.contacto@gmail.com'
PASSW = 'xoejdavfzdfnoigf'

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def home(response):
    return render(response,'home.html')

def infoPersonal(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 1 :
        response.session.flush()
        return redirect('/')
    o= User.objects.all()
    idu=response.session["user_id"]
    usu=o.get(id=idu)
    edad = calculate_age(usu.birthDate)
    return render(response,'visualizarInfoPersonal.html', {"usuario":usu,"edad":edad})

def modificarInfo(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 1 :
        response.session.flush()
        return redirect('/')
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

def registerCentro(response):
    form = RegisterCentro()
    if(response.method == "POST"):
            form = RegisterCentro(response.POST)
            if form.is_valid():
                data = form.cleaned_data
                response.session["center"] = data["center"]
                completarUsuario(response)
                return enviaremailNormal(response)

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
        return redirect('/login')     

def enviaremailNormal(response): 
    
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

        smtp.sendmail(EMAIL, DESTINATARIO, msg)                                      #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion


    response.session.flush()
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

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
        user.appointment_set.create(state=0,center=user.center,vaccine=vacC,edad=calculate_age(user.birthdate))

    if (user.history.gripe == '0'):
        vacG = Vaccine.objects.get(name="Gripe")
        user.appointment_set.create(state=0,center=user.center,vaccine=vacG,edad=calculate_age(user.birthdate))
    elif (calculate_age(datetime.strptime(user.history.gripe_date, '%Y-%m-%d').date()) > 0):
        vacG = Vaccine.objects.get(name="Gripe")
        user.appointment_set.create(state=0,center=user.center,vaccine=vacG,edad=calculate_age(user.birthdate))  
    
def visualizar(response):
    return render(response,'visualizarInfoPersonal.html')

def CerrarSesion(response):
    if not checkearLogin(response):
        return redirect('/')
    response.session.flush()
    return redirect('http://127.0.0.1:8000/')

def homeUsuario(response):
    if not checkearLogin(response):
        return redirect('/')
    o= User.objects.all()
    idu=response.session["user_id"]
    usu=o.get(id=idu)
    if(usu.is_staff):
         response.session["usubuscar"]=0
         response.session["ok"]=0
         response.session["categoria"]=2
         return redirect('/homeAdminCentro')     
    else:
        if(usu.is_admin):
            response.session["categoria"]=3
            return redirect('/turnosParaAsignar/centro/1')   
        else:
            NCOMPLETO = usu.name + ' ' + usu.surname
            turnos = usu.appointment_set.all()
            fiebre_disp = False
            vacF = Vaccine.objects.get(name="Fiebre Amarilla")
            if ((usu.history.fiebreA == False)) and (calculate_age(usu.birthDate) < 60):
                if( not tieneTurno(usu,vacF)):
                    fiebre_disp = True   
            response.session["categoria"]=1         
            return render(response,'inicioPaciente.html', {'NOMBRE': NCOMPLETO, 'turnos': turnos, 'fiebre_disp':fiebre_disp,'user':usu,'dosis':(usu.history.covid_doses + 1)})
    
def modificarContraseña(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] == 3 :
        response.session.flush()
        return redirect('/')
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
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 1 :
        response.session.flush()
        return redirect('/')
    o= User.objects.all()
    idu=response.session["user_id"]
    usu=o.get(id=idu)
    vacF = Vaccine.objects.get(name="Fiebre Amarilla")
    turnoF = Appointment(state=0,center=usu.center,vaccine=vacF,patient=usu,edad=calculate_age(usu.birthdate))
    turnoF.save()
    return redirect('/homeUsuario')

def tieneTurno(user,vacuna):  # se puede usar con cualquier vacuna, el segundo parametro tiene que ser el objeto de la vacuna
    tiene = False
    for turno in user.appointment_set.all():
        if turno.vaccine == vacuna:
            tiene = True
    return tiene

def validarUsuRecuperar(response):
    mail=response.POST['mail']
    o=User.objects.all()
    usu=o.filter(email=mail).exists()
    if usu:
        token=response.POST['token']
        usu=o.get(email=mail)
        if usu.token==token:
            response.session['email']=mail
            return mailRecuperarContraseña(response)
        else:
            messages.warning(response, 'El token no es el correcto.')
    else:
        messages.warning(response, 'El mail ingresado no pertenece a ningun usuario.')
    return redirect('http://127.0.0.1:8000/recuContraseña') 

def validarCambioContraseñaRecuperada(response):
    mail=response.POST['mail']
    o=User.objects.all()
    usu=o.filter(email=mail).exists()
    if usu:
        usu=o.get(email=mail)
        cn=response.POST['contNueva']
        cnr=response.POST['contNuevaR']
        upper = False
        for character in cn:
            if character.isupper():
                upper = True
        if(not upper):
            messages.warning(response, 'La contraseña nueva debe contener al menos una letra mayuscula')
        else:
            if check_password(cn, usu.password):
                messages.warning(response, 'La contraseña ingreso es igual a la anterior.')
            elif cn==cnr:
                usu.set_password(cn)
                usu.save()
                response.session.flush()
                messages.warning(response, 'La contraseña se a cambiado de manera exitosa.')
                return redirect('http://127.0.0.1:8000/login') 
            else:
                messages.warning(response, 'La contraseña nueva y la repetida deben ser iguales.')
    else:
        messages.warning(response, 'Mail incorrecto.')
    return redirect('http://127.0.0.1:8000/camcontrecu') 

    NOMBRE = usu.name
    APELLIDO = usu.surname
    NCOMPLETO = NOMBRE + ' ' + APELLIDO
    return render(response,'inicioPaciente.html', {'NOMBRE': NCOMPLETO})

def validarCambioMail(response):
        if not checkearLogin(response):
            return redirect('/')
        if response.session["categoria"] != 1 :
            response.session.flush()
            return redirect('/')
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
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 1 :
            response.session.flush()
            return redirect('/')
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

def elegirCertificado(response):
    return render(response,'elegirCertificado.html')
#Creating a class based view
class PdfGripe(View):
     def get(self, response, *args, **kwargs):
        if not checkearLogin(response):
            return redirect('/')
        turnoG = None 
        user = User.objects.get(id= response.session["user_id"])
        #certificado gripe
        if user.history.gripe == 1:

            turnoG = user.appointment_set.filter(vaccine = 2).order_by('-date')
            if len(turnoG) > 0:
                turnoG = turnoG[0]
            else:
                turnoG = None
        open('vacuApp/templates/temp.html', "w",encoding='utf-8').write(render_to_string('certifGripe.html', {'turnoG' : turnoG}))
        pdf = html_to_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
class PdfFiebreA(View):
     def get(self, response, *args, **kwargs):
        if not checkearLogin(response):
            return redirect('/')   
        turnoF = None
        user = User.objects.get(id= response.session["user_id"])
        if user.history.fiebreA == 1:
            turnoF = user.appointment_set.filter(vaccine = 3).order_by('-date')
            if len(turnoF) > 0:
                turnoF = turnoF[0]
            else:
                turnoF = None
        open('vacuApp/templates/temp.html', "w",encoding='utf-8').write(render_to_string('certifFiebreA.html', {'turnoF' : turnoF}))
        pdf = html_to_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')
class PdfCovid(View):
     def get(self, response, *args, **kwargs):
        if not checkearLogin(response):
            return redirect('/')   
        user = User.objects.get(id= response.session["user_id"])
        turnoC = None
        dosis = None
        if user.history.covid_doses > 0:
            turnoC = user.appointment_set.filter(vaccine = 1).order_by('-date')
            if len(turnoC) > 0:
                turnoC = turnoC[0]
                dosis = user.history.covid_doses
            else:
                turnoF = None
        open('vacuApp/templates/temp.html', "w",encoding='utf-8').write(render_to_string('certifCovid.html', {'turnoC':turnoC, 'dosis': dosis}))

        # getting the template
        pdf = html_to_pdf('temp.html')
         
         # rendering the template
        return HttpResponse(pdf, content_type='application/pdf')

def borrarRegistro(response):
    o= User.objects.all()
    if o!=None:
        idUsuario = response.session['reg_user_id']
        usu = o.get(id = idUsuario)
        usu.delete() 
        messages.info(response, "Se ha cancelado el registro" )                 
        return redirect('/')              
    else:
        messages.error(response, 'No hay usuarios cargados en la base')  
    return redirect('/')

def homeAdmin(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 2 :
        response.session.flush()
        return redirect('/')
    o= User.objects.all()
    idUsuario = response.session["user_id"]
    usu = o.get(id = idUsuario)
    NCOMPLETO = usu.name + ' ' + usu.surname
    messages.success(response, ' Bienvenid@ a VacunAssist '+NCOMPLETO)
    t=Appointment.objects.all()
    print(t)
    today = date.today()
    #covid
    turnosC=t.filter(vaccine=1,state=1,center=1,date=today)
    print (turnosC)
    dtc=t.filter(vaccine=1,center=usu.center,date=today).exclude(state=1)
    if (not dtc):
        dtc=0
    print (dtc)
    if (not turnosC):
        turnosC=0
        cantC=0
    else:
        cantC=t.filter(vaccine=1,state=1,center=usu.center,date=today).count()
    #gripe
    turnosG=t.filter(vaccine=2,state=1,center=usu.center,date=today)
    print (turnosG)
    dtg=t.filter(vaccine=2,center=usu.center,date=today).exclude(state=1)
    if(not dtg):
        dtg=0
    if (not turnosG):
        turnosG=0
        cantG=0
    else:
        cantG=t.filter(vaccine=2,state=1,center=usu.center,date=today).count()
    #fiebre
    turnosF=t.filter(vaccine=3,state=1,center=usu.center,date=today)
    print (turnosF)
    dtf=t.filter(vaccine=3,center=usu.center,date=today).exclude(state=1)
    if(not dtf):
        dtf=0
    if (not turnosF):
        turnosF=0
        cantF=0
    else:
        cantF=t.filter(vaccine=3, state=1, center=usu.center,date=today).count()
    tot=cantC+cantG+cantF
    #buscar
    usubuscado=0
    if (response.session["usubuscar"] == 1):
        response.session["usubuscar"]=0
        dni=response.session["dni"]
        response.session["dni"]=-1
        o=User.objects.all()
        u=o.filter(DNI=dni).exists()
        if (u):
            u=o.get(DNI=dni)
            today = date.today()
            t=u.appointment_set.filter(state=1,date=today,center=usu.center).exists()
            if(t):
                t=u.appointment_set.get(state=1,date=today,center=usu.center)
                usubuscado=t 
            else:
                usubuscado=1
        else:
            usubuscado=2
    return render(response,'inicioAdminCentro.html', {'turnobuscado':usubuscado,'tot':tot,'hoy':today, 'covid':turnosC, 'cantC':cantC, 'demasC':dtc, 'gripe':turnosG,'cantG':cantG,'demasG':dtg, 'fiebre':turnosF,'cantF':cantF,'demasF':dtf,'ok': response.session["ok"]})

def presente(response,id,tipo):
    if not checkearLogin(response):
        return redirect('/') 
    if response.session["categoria"] != 2 :
        response.session.flush()
        return redirect('/')
    observaciones = response.POST["observaciones"]
    detalles = response.POST["detalles"]
    T = Appointment.objects.all()
    turnoActual = T.get(id = id)
    turnoActual.state = 2
    turnoActual.observaciones = observaciones
    turnoActual.descripcion = detalles
    H = History.objects.all()
    usu = User.objects.get(id = turnoActual.patient_id)
    historialActual = H.get(user_id = usu.id)
    if (tipo == 1): 
        historialActual.covid_date = datetime.today().strftime('%Y-%m-%d')
        historialActual.covid_doses += 1
        if(historialActual.covid_doses < 2):
            vacC = Vaccine.objects.get(name="Covid")
            usu.appointment_set.create(state=0,center=usu.center,vaccine=vacC,edad=calculate_age(usu.birthdate))
    else:
        if (tipo == 2):
            historialActual.gripe_date = datetime.today().strftime('%Y-%m-%d')
            historialActual.gripe = True
        else:     
            historialActual.fiebreA_date = datetime.today().strftime('%Y-%m-%d')
            historialActual.fiebreA_date
            
    turnoActual.save()
    historialActual.save()                
    return redirect('http://127.0.0.1:8000/homeAdminCentro')

def marcarTurnoAusentes(response):
        if not checkearLogin(response):
            return redirect('/')
        if response.session["categoria"] != 2 :
            response.session.flush()
            return redirect('/')
        if(response.session["ok"] == 0):
            response.session["ok"]=1
            return redirect('http://127.0.0.1:8000/homeAdminCentro')  
        else:
            respuesta=response.POST["respuesta"]
            if(respuesta=='SI'):
                today = date.today()
                o= User.objects.all()
                usu=o.get(id=response.session["user_id"])
                t=Appointment.objects.all()
                ausentes=t.filter(state=1, center=usu.center,date=today) #,date=today
                if(len(ausentes) > 0):
                    for turno in ausentes:
                        turno.state=0
                        turno.cancel=1
                        turno.save()
                else:
                    messages.error(response,"No hay turnos para marcar como ausentes")
            response.session["ok"]=0
        return redirect('/homeAdminCentro')

def pasarAadminiReiniciarbuscarUsuario(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 2 :
        response.session.flush()
        return redirect('/')
    response.session["dni"]=response.POST["dni"]
    if (response.session["usubuscar"]==0):
        response.session["usubuscar"]=1
    return redirect('http://127.0.0.1:8000/homeAdminCentro')

def checkearLogin(response):
    return "user_id" in response.session
        
def informacionVacunas(response):
    return render(response,'infoVacunas.html')

def completarVacunas(response,id,tipo):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 2 :
        response.session.flush()
        return redirect('/')
    T = Appointment.objects.all()
    turnoActual = T.get(id = id)
    usu = User.objects.get(id = turnoActual.patient_id)
    NCOMPLETO = usu.name + ' ' + usu.surname
    return render(response,'completarTurnoVacuna.html', {'idApp':id,'tipoVacuna':tipo, 'nombre': NCOMPLETO})

def modificarCentro(response, id):
    return render(response,'ingresarNuevaInfoCentro.html', {'centro':id})

def modificar(response, id):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    nombreNuevo = response.POST["nombre"]
    direccNueva = response.POST["direccion"]
    c = Center.objects.get(id = id)
    if (nombreNuevo == "") and (direccNueva == ""):
            messages.info(response,'No hay informacion nueva que cargar')
    else:     
        if (nombreNuevo != ""):
            if (c.name == nombreNuevo):
                messages.error(response,'El nombre no puede ser el actual')
                return render(response,'ingresarNuevaInfoCentro.html', {'centro':id}) 
            else:
                todosLosCentros = Center.objects.all()
                cCopiado = todosLosCentros.filter(name = nombreNuevo)    
                if cCopiado:
                    messages.warning(response, 'El nombre nuevo coincide con el de otro centro')
                    return render(response,'ingresarNuevaInfoCentro.html', {'centro':id})
                else:
                    messages.success(response,'Nombre modificado con exito')
                    c.name = nombreNuevo
        if (direccNueva != ""):
            if (c.adress == direccNueva):
                messages.error(response,'La direccion nueva no puede ser la actual')
                return render(response,'ingresarNuevaInfoCentro.html', {'centro':id}) 
            else:
                todosLosCentros = Center.objects.all()
                cCopiado = todosLosCentros.filter(adress = direccNueva)    
                if cCopiado:
                    messages.warning(response, 'La direccion nueva coincide con la de otro centro')
                    return render(response,'ingresarNuevaInfoCentro.html', {'centro':id})
                else:
                    messages.success(response,'Direccion modificada con exito')
                    c.adress = direccNueva
        c.save()
    centros = Center.objects.all()
    a = User.objects.filter(is_staff = 1)
    return render(response,'seleccionar.html',{'todosLosAdmins':a, 'todosLosCentros': centros})

def enviaremail(response, admin, CLAVE): 
    
    #user = request.session["user"]
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:                               #Esto prepara la conexion con gmail, utilizando el puerto 587, y lo llamamos smtp 
        DESTINATARIO = admin.email
        smtp.ehlo()                                                                 #Nos identifica con gmail
        smtp.starttls()                                                             #Encripta algo que no se como se llama
        smtp.ehlo()                                                                 #Nos identificamos de nuevo porque nos encriptamos    
        smtp.login(EMAIL, PASSW)                                                    #Nos logeamos (xoejdavfzdfnoigf)
        TOKEN = random.randint(1000, 9999)
        admin.token = TOKEN
        admin.save()
        subject = 'Confirmacion de cuenta'                                          #Asunto del email
        body = 'Este es un mensage autogenerado por VacunAssist. Para acceder a su cuenta utilice la siguiente clave ' + str(CLAVE) + ',su TOKEN es ' + str(TOKEN)          
        msg = f'Subject: {subject}\n\n{body}'                                       #Es necesario formatear el mensaje (f) para que lo tome gmail
        smtp.sendmail(EMAIL, DESTINATARIO, msg)                                     #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion
    response.session.flush()
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def crearAdmin(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    centros = Center.objects.all()
    return render(response,'crearAdmin.html', {'todosLosCentros': centros})
    
def completarAdmin(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    nombreNuevo = response.POST["nombre"]
    apellidoNuevo = response.POST["apellido"]
    emailNuevo = response.POST["email"]
    dniNuevo = response.POST["dni"]
    o= User.objects.all()
    usu = o.filter(email=emailNuevo)
    if usu:
        messages.error(response, 'El mail pertenece a otra cuenta del sistema')
        centros = Center.objects.all()
        return render(response,'crearAdmin.html', {'todosLosCentros': centros})
    else:  
        usu = o.filter(DNI = dniNuevo)
        if usu:
            messages.error(response, 'El DNI pertenece a otra cuenta del sistema')
            centros = Center.objects.all()
            return render(response,'crearAdmin.html', {'todosLosCentros': centros}) 
        else:
            c = Center.objects.get(id = response.POST.get('elegido'))
            adminNuevo = User(id= (User.objects.count() + 1), name= nombreNuevo, surname= apellidoNuevo, email= emailNuevo, birthDate= '2000-06-05', DNI= dniNuevo, center_id= c.id, is_staff= True, is_admin=False)
            CLAVE = str(random.randint( 1000000, 9999999)) + str("V")
            AUX = CLAVE
            adminNuevo.set_password(CLAVE)
            adminNuevo.save()
            enviaremail(response, adminNuevo, AUX)
            messages.success(response, 'Se ha creado un nuevo administrador de centro')
            a = User.objects.filter(is_staff = 1)
            centros = Center.objects.all()
            return render(response,'seleccionar.html',{'todosLosAdmins':a, 'todosLosCentros': centros, 'totalAdmins': a.count()})

def elegirGrafico(response):
    return render(response,'elegirGrafico.html')

def graficoCentros(response):
    centros = Center.objects.all()
    turnos = Appointment.objects.all()
    #cantidad de turnos por centro
    canttotalturnos = []
    Ncentroscanttotalturnos = []
    for centro in centros:
        cant = turnos.filter(center = centro).count()
        canttotalturnos.append(cant)
        Ncentroscanttotalturnos.append(centro.name)
    #cantidad de turnos pendientes por centro
    cantpendienteturnos = [] 
    Ncentrospendienteturnos = []
    for centro in centros:
        cant = turnos.filter(center = centro, state=0, cancel=False).count()
        cantpendienteturnos.append(cant)
        Ncentrospendienteturnos.append(centro.name)
    #cantidad de turnos asignados
    cantasignadoturnos = [] 
    Ncentrosasignadoturnos = []
    for centro in centros:
        cant = turnos.filter(center = centro, state=1).count()
        cantasignadoturnos.append(cant)
        Ncentrosasignadoturnos.append(centro.name)
    #cantidad de turnos asistidos
    cantasistidosturnos = [] 
    Ncentrosasistidosturnos = []
    for centro in centros:
        cant = turnos.filter(center = centro, state=2).count()
        cantasistidosturnos.append(cant)
        Ncentrosasistidosturnos.append(centro.name)
    #cantidad de turnos ausentes
    cantausentesturnos = [] 
    Ncentrosausentesturnos = []
    for centro in centros:
        cant = turnos.filter(center = centro, state=0, cancel=True).count()
        cantausentesturnos.append(cant)
        Ncentrosausentesturnos.append(centro.name)
    #cantidad de personas por centro
    canttotpersonas = [] 
    Ncentrostotpersonas = []
    personas=User.objects.all()
    for centro in centros:
        cant = personas.filter(is_staff=False, is_admin=False, center = centro).count()
        canttotpersonas.append(cant)
        Ncentrostotpersonas.append(centro.name)
    return render(response,'graficoCentros.html',{'Nct':Ncentroscanttotalturnos,'Ctt':canttotalturnos,
    'Npt':Ncentrospendienteturnos,'Cpt':cantpendienteturnos,
    'Nat':Ncentrosasignadoturnos,'Cat':cantasignadoturnos,
    'Nast':Ncentrosasistidosturnos,'Cast':cantasistidosturnos,
    'Naut':Ncentrosausentesturnos,'Caut':cantausentesturnos,
    'Np':Ncentrostotpersonas,'Cp':canttotpersonas,})

def graficoVacunas(response):
    vacunas = Vaccine.objects.all()
    turnos = Appointment.objects.all()
    #total de turnos por vacuna
    canttotalturnosvacunas = []
    Nvacunascanttotalturnos = []
    for vacuna in vacunas:
        cant = turnos.filter(vaccine = vacuna).count()
        canttotalturnosvacunas.append(cant)
        Nvacunascanttotalturnos.append(vacuna.name)
    #total personas vacunadas   
    canttotalpersonasvacunas = []
    Nvacunascanttotalpersonas = []
    personas=User.objects.all()
    for vacuna in vacunas:
        cant=0
        for persona in personas:
            if turnos.filter(patient=persona,vaccine=vacuna,state=2).exists():
                cant=cant+1
        canttotalpersonasvacunas.append(cant)
        Nvacunascanttotalpersonas.append(vacuna.name)
    #total cantidad vacunas aplicadas 
    canttotalvacunasapli = []
    Nvacunascanttotalapli = []
    personas=User.objects.all()
    for vacuna in vacunas:
        cant=turnos.filter(vaccine=vacuna,state=2).count()
        canttotalvacunasapli.append(cant)
        Nvacunascanttotalapli.append(vacuna.name)
    #total cantidad de vacunas pendientes a aplicacion  
    canttotalvacunaspend = []
    Nvacunascanttotalpend = []
    personas=User.objects.all()
    for vacuna in vacunas:
        cant = turnos.filter(vaccine = vacuna,state=1).count()
        canttotalvacunaspend.append(cant)
        Nvacunascanttotalpend.append(vacuna.name)
    #total cantidad aplicaciones canceladas por vacunas  
    canttotalvacunascanc = []
    Nvacunascanttotalcanc = []
    personas=User.objects.all()
    for vacuna in vacunas:
        cant = turnos.filter(vaccine = vacuna,state=0,cancel=False).count()
        canttotalvacunascanc.append(cant)
        Nvacunascanttotalcanc.append(vacuna.name)
    return render(response,'graficoVacunas.html',{'Ntv':Nvacunascanttotalturnos,'Ctv':canttotalturnosvacunas,
    'Npv':Nvacunascanttotalpersonas,'Cpv':canttotalpersonasvacunas,
    'Nav':Nvacunascanttotalapli,'Cav':canttotalvacunasapli,
    'Npnv':Nvacunascanttotalpend,'Cpnv':canttotalvacunaspend,
    'Ncv':Nvacunascanttotalcanc,'Ccv':canttotalvacunascanc,})

def graficoUsuarios(response):
    centros = Center.objects.all()
    turnos = Appointment.objects.all()
    usuarios = User.objects.all()
    #cantidad de personas registradas en el sistemas por sexo
    cantsexo = []
    Nsexo = []
    cant = usuarios.filter(sex='M').count()
    cantsexo.append(cant)
    Nsexo.append('M')
    cant = usuarios.filter(sex='F').count()
    cantsexo.append(cant)
    Nsexo.append('F')
    #cantidad de personas con turnos asignados o pendientes
    cantpenoasig = []
    Npenoasig = []
    p=0
    a=0  
    for usuario in usuarios:
        if usuario.is_admin==False and usuario.is_staff==False :
            if turnos.filter(patient=usuario,state=0).exists():
                p=p+1
            if turnos.filter(patient=usuario,state=1).exists():
                a=a+1    
    cantpenoasig.append(p)
    Npenoasig.append('Pendientes')
    cantpenoasig.append(a)
    Npenoasig.append('Asignados')
    #cantidad de personas con turnos cancelados o completos
    cantcancelopres = []
    Ncancelopres = []
    c=0
    a=0  
    for usuario in usuarios:
        if usuario.is_admin==False and usuario.is_staff==False :
            if turnos.filter(patient=usuario,state=0,cancel=True).exists():
                c=c+1
            if turnos.filter(patient=usuario,state=2).exists():
                a=a+1    
    cantcancelopres.append(c)
    Ncancelopres.append('Ausentes')
    cantcancelopres.append(a)
    Ncancelopres.append('Presentes')
    #cantidad de personas registradas en el sistemas por por rango de edad
    cantrangoedad = []
    Nrangoedad = []
    uno=0; dos=0; tres=0; cuatro=0; cinco=0
    for usu in usuarios:
        if usu.is_admin==False and usu.is_staff==False :
            edad= calculate_age(usu.birthDate)
            if (edad<18):
                uno=uno+1
            else:
                if(edad>=18 and edad<30):
                    dos=dos+1
                else:
                    if(edad>=30 and edad<50):
                        tres=tres+1
                    else:
                        if(edad>=50 and edad<70):
                            cuatro=cuatro+1
                        else:
                            cinco=cinco+1
    cantrangoedad.append(uno)
    Nrangoedad.append('Menos de 18')
    cantrangoedad.append(dos)
    Nrangoedad.append('De 18 a menos de 30')
    cantrangoedad.append(tres)
    Nrangoedad.append('De 30 a menos de 50  ')
    cantrangoedad.append(cuatro)
    Nrangoedad.append('De 50 a menos de 70')
    cantrangoedad.append(cinco)
    Nrangoedad.append('De 70 a mas')
    return render(response,'graficoUsuarios.html',{'Nrs':Nsexo,'Crs':cantsexo,
    'Npa':Npenoasig,'Cpa':cantpenoasig,
    'Ncp':Ncancelopres,'Ccp':cantcancelopres,
    'Ne':Nrangoedad,'Ce':cantrangoedad,
    })

def turnosParaAsignar(response,pagina=1,filtro='centro'):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    turnos = Appointment.objects.filter(state = 0)
    fecha = None
    cantidades = None
    if response.method == "POST":
        fecha = response.POST["fecha"]
        message = validators.validarFechaAsginar(fecha)
        if message == '':
            cantidades = turnosPorCentro(fecha)
        else: 
            fecha = None
            messages.error(response,message)
    if(filtro == 'fecha'):
        turnos = turnos.order_by('date')
    elif(filtro == 'nombre'):
        turnos = turnos.order_by('patient__surname')
    elif(filtro == 'vacuna'):
        turnos = turnos.order_by('vaccine__name')
    elif(filtro == 'edad'):
        turnos = turnos.order_by('edad')
    else:
        turnos = turnos.order_by('center__name')
    p = Paginator(turnos,12)
    pagina_actual = p.page(pagina)
    return render(response,'turnosParaAsignar.html',{'pagina':pagina_actual,'paginas':p,'fecha':fecha,'filtro':filtro,'cantidades':cantidades})

def turnosPorCentro(fecha):
    centros = Center.objects.all()
    turnos = Appointment.objects.filter(state = 1,date = fecha)
    vacC = Vaccine.objects.get(id = 1)
    vacG = Vaccine.objects.get(id = 2)
    vacF = Vaccine.objects.get(id = 3)
    dic = {}    
    for centro in centros:
        arr = []
        arr.append("Covid:")
        arr.append(turnos.filter(center = centro,vaccine = vacC).count())
        arr.append("Gripe:")
        arr.append(turnos.filter(center = centro,vaccine = vacG).count())
        arr.append("Fiebre Amarilla:")
        arr.append(turnos.filter(center = centro,vaccine = vacF).count())
        dic[centro.name] = arr
    return dic
    
def asignarTurnos(response,fecha,pagina,filtro):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    turnos = response.POST.getlist("turnos[]")
    print(turnos)
    for turno in turnos:
        turnobj = Appointment.objects.get(id = turno)
        message = validators.validarTurnoMismoDia(turnobj.patient,fecha)
        if message == '':
            turnobj.state = 1
            turnobj.date = fecha
            turnobj.save()
        else:
            messages.error(response,message)
    turnos = Appointment.objects.filter(state = 0)
    p = Paginator(turnos,12)
    pagina_actual = p.page(pagina)
    cantidades = turnosPorCentro(fecha)
    return render(response,'turnosParaAsignar.html',{'pagina':pagina_actual,'paginas':p,'fecha':fecha,'filtro':filtro,'cantidades':cantidades})

def turnosAsignados(response,pagina = 1,filtro='centro'):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    turnos = Appointment.objects.filter(state = 1)
    if(filtro == 'fecha'):
        turnos = turnos.order_by('date')
    elif(filtro == 'nombre'):
        turnos = turnos.order_by('patient__surname')
    elif(filtro == 'vacuna'):
        turnos = turnos.order_by('vaccine__name')
    else:
        turnos = turnos.order_by('center__name')
    p = Paginator(turnos,12)
    pagina_actual = p.page(pagina)
    return render(response,'turnosAsignados.html',{'pagina':pagina_actual,'paginas':p})

def cancelarTurno(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    turno = Appointment.objects.get(id = response.POST["turno"])
    turno.state = 0
    turno.date = None
    turno.save()
    return redirect('/turnosAsignados')

    
def mailRecuperarContraseña(response):
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:                               #Esto prepara la conexion con gmail, utilizando el puerto 587, y lo llamamos smtp 
        user = User.objects.get(email=response.session["email"]) 
        NAME = user.name
        SURNAME =  user.surname
        NCOMPLETO = str(NAME) + ' ' + str(SURNAME)
        DESTINATARIO = response.session["email"]
        user.save()

        smtp.ehlo()                                                                 #Nos identifica con gmail
        smtp.starttls()                                                             #Encripta algo que no se como se llama
        smtp.ehlo()                                                                 #Nos identificamos de nuevo porque nos encriptamos    
        smtp.login(EMAIL, PASSW)     
                                                       #Nos logeamos (xoejdavfzdfnoigf)
        subject = 'Recuperar Cuenta'                                          #Asunto del email
        body = 'Para recuparar su cuenta haga click en el siguiente link:  http://127.0.0.1:8000/camcontrecu '          
        msg = f'Subject: {subject}\n\n{body}'                                       #Es necesario formatear el mensaje (f) para que lo tome gmail

        smtp.sendmail(EMAIL, DESTINATARIO, msg)                                       #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion

    return HttpResponse("""<html><script>window.location.replace('/envioMailRecuperar');</script></html>""")

def verEnvioMailRecuperar(responde):
    return render(responde, 'recuperarcontesperandomail.html')

def borrarAdmin(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    a = User.objects.filter(is_staff = 1)
    return render(response,'borrarAdminX.html',{'todosLosAdmins':a})

def selec(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    a = User.objects.filter(is_staff = 1)
    centros = Center.objects.all()
    return render(response,'seleccionar.html',{'todosLosAdmins':a, 'todosLosCentros': centros, 'totalAdmins': a.count(),'seQuiereEliminar': 0})

def modificarAdminC(response, id):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    c = Center.objects.all()
    return render(response,'modificarInfoAdminC.html', {'elegido':id,'todosLosCentros': c})

def modificarAdminX(response, id):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] == 3 :
        response.session.flush()
        return redirect('/')
    nomN = response.POST["nombreN"]
    apeN = response.POST["apellidoN"]
    dniN = response.POST["dniN"]
    centroN = response.POST["centroN"]
    admin = User.objects.get(id = id)
    a = User.objects.filter(is_staff = 1)
    centros = Center.objects.all()
    if (nomN == '') and (apeN == '') and (dniN == '') and (centroN == ''):
        messages.info(response, 'No se hicieron cambios')
        return render(response,'seleccionar.html',{'todosLosAdmins':a, 'todosLosCentros': centros, 'totalAdmins': a.count()})
    else:
        if (nomN != ''):
            if (admin.name == nomN):
                messages.error(response, 'El nombre nuevo no puede ser el actual')
                return render(response,'modificarInfoAdminC.html', {'elegido':id,'todosLosCentros': centros})
            else:
                admin.name = nomN
        if (apeN != ''):
            if (admin.surname == apeN):
                messages.error(response, 'El apellido nuevo no puede ser el actual')
                return render(response,'modificarInfoAdminC.html', {'elegido':id,'todosLosCentros': centros})
            else:
                admin.surname = apeN
        if (dniN != ''):
            if (admin.DNI == dniN):
                messages.error(response, 'El DNI nuevo no puede ser el actual')
                return render(response,'modificarInfoAdminC.html', {'elegido':id,'todosLosCentros': centros})
            else:
                copiado = User.objects.filter(DNI = dniN)
                if copiado:
                    messages.error(response, 'El DNI pertenece a otro usuario del sistema')
                    return render(response,'modificarInfoAdminC.html', {'elegido':id,'todosLosCentros': centros})
                else:
                    admin.DNI = dniN
        if (centroN != ''):
            existe = Center.objects.filter(name = centroN)
            if existe:
                if (admin.center == existe):
                    messages.error(response, 'El centro nuevo no puede ser el actual')
                    return render(response,'modificarInfoAdminC.html', {'elegido':id,'todosLosCentros': centros})
                else:
                    cNuevo = Center.objects.get(name = centroN)
                    admin.center_id = cNuevo.id
            else:
                messages.error(response, 'El centro ingresado no existe')
                return render(response,'modificarInfoAdminC.html', {'elegido':id,'todosLosCentros': centros})
        messages.success(response, 'Se han modificado los datos correctamente')
        admin.save()
    return render(response,'seleccionar.html',{'todosLosAdmins':a, 'todosLosCentros': centros, 'totalAdmins': a.count()})

def confirmarEliminar(response,id):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    a = User.objects.filter(is_staff = 1)
    centros = Center.objects.all()
    return render(response,'seleccionar.html',{'todosLosAdmins':a, 'todosLosCentros': centros, 'totalAdmins': a.count(),'seQuiereEliminar': 1, 'afectado': id})

def eliminarAdmin(response,id):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 3 :
        response.session.flush()
        return redirect('/')
    a = User.objects.filter(is_staff = 1)
    centros = Center.objects.all()
    respuesta=response.POST["respuesta"]
    if(respuesta=='SI'):
        admin = User.objects.filter (id = id)
        admin.delete()
        messages.success(response, 'Se ha eliminado el administrador')
    else:
        messages.info(response, 'No se hicieron cambios')
    return render(response,'seleccionar.html',{'todosLosAdmins':a, 'todosLosCentros': centros, 'totalAdmins': a.count(),'seQuiereEliminar': 0})

def miInfo(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 2 :
        response.session.flush()
        return redirect('/')
    o= User.objects.all()
    miId = response.session["user_id"]
    yo = o.get(id = miId)
    return render(response,'miInfo.html', {'miNombre': yo.name, 'miApellido': yo.surname, 'miDNI': yo.DNI, 'miEmail': yo.email})

def modificarMiInfo(response):
    if not checkearLogin(response):
        return redirect('/')
    if response.session["categoria"] != 2 :
        response.session.flush()
        return redirect('/')
    nomN = response.POST["nombreN"]
    apeN = response.POST["apellidoN"]
    dniN = response.POST["dniN"]
    emailN = response.POST["emailN"]
    miId = response.session["user_id"]
    admin = User.objects.get(id = miId)
    a = User.objects.filter(is_staff = 1)
    o= User.objects.all()
    miId = response.session["user_id"]
    yo = o.get(id = miId)
    idUsuario = response.session["user_id"]
    usu = o.get(id = idUsuario)
    usubuscado=0
    today = date.today()
    t=Appointment.objects.all()
    turnosC=t.filter(vaccine=1,state=1,center=usu.center,date=today)
    dtc=t.filter(vaccine=1,center=usu.center,date=today).exclude(state=1)
    turnosG=t.filter(vaccine=2,state=1,center=usu.center,date=today)
    dtg=t.filter(vaccine=2,center=usu.center,date=today).exclude(state=1)
    turnosF=t.filter(vaccine=3,state=1,center=usu.center,date=today)
    dtf=t.filter(vaccine=3,center=usu.center,date=today).exclude(state=1)
    if(not dtf):
        dtf=0
    if (not turnosF):
        turnosF=0
        cantF=0
    else:
        cantF=t.filter(vaccine=3, state=1, center=usu.center,date=today).count()
    if(not dtg):
        dtg=0
    if (not turnosG):
        turnosG=0
        cantG=0
    else:
        cantG=t.filter(vaccine=2,state=1,center=usu.center,date=today).count()
    print (dtc)
    if (not dtc):
        dtc=0
    if (not turnosC):
        turnosC=0
        cantC=0
    else:
        cantC=t.filter(vaccine=1,state=1,center=usu.center,date=today).count()
    tot=cantC+cantG+cantF
    if (nomN == '') and (apeN == '') and (dniN == '') and (emailN == ''):
        messages.info(response, 'No se hicieron cambios')
        return render(response,'inicioAdminCentro.html', {'turnobuscado':usubuscado,'tot':tot,'hoy':today, 'covid':turnosC, 'cantC':cantC, 'demasC':dtc, 'gripe':turnosG,'cantG':cantG,'demasG':dtg, 'fiebre':turnosF,'cantF':cantF,'demasF':dtf,'ok': response.session["ok"]})
    else:
        if (nomN != ''):
            if (admin.name == nomN):
                messages.error(response, 'El nombre nuevo no puede ser el actual')
                return render(response,'miInfo.html', {'miNombre': yo.name, 'miApellido': yo.surname, 'miDNI': yo.DNI, 'miEmail': yo.email})
            else:
                admin.name = nomN
        if (apeN != ''):
            if (admin.surname == apeN):
                messages.error(response, 'El apellido nuevo no puede ser el actual')
                return render(response,'miInfo.html', {'miNombre': yo.name, 'miApellido': yo.surname, 'miDNI': yo.DNI, 'miEmail': yo.email})
            else:
                admin.surname = apeN
        if (dniN != ''):
            if (admin.DNI == dniN):
                messages.error(response, 'El DNI nuevo no puede ser el actual')
                return render(response,'miInfo.html', {'miNombre': yo.name, 'miApellido': yo.surname, 'miDNI': yo.DNI, 'miEmail': yo.email})
            else:
                copiado = User.objects.filter(DNI = dniN)
                if copiado:
                    messages.error(response, 'El DNI pertenece a otro usuario del sistema')
                    return render(response,'miInfo.html', {'miNombre': yo.name, 'miApellido': yo.surname, 'miDNI': yo.DNI, 'miEmail': yo.email})
                else:
                    admin.DNI = dniN
        if (emailN != ''):
            if (admin.email == emailN):
                messages.error(response, 'El email nuevo no puede ser el actual')
                return render(response,'miInfo.html', {'miNombre': yo.name, 'miApellido': yo.surname, 'miDNI': yo.DNI, 'miEmail': yo.email})
            else:
                copiado = User.objects.filter(email = emailN)
                if copiado:
                    messages.error(response, 'El email pertenece a otro usuario del sistema')
                    return render(response,'miInfo.html', {'miNombre': yo.name, 'miApellido': yo.surname, 'miDNI': yo.DNI, 'miEmail': yo.email})
                else:
                    admin.email = emailN
        messages.success(response, 'Se han modificado los datos correctamente')
        admin.save()
    return render(response,'inicioAdminCentro.html', {'turnobuscado':usubuscado,'tot':tot,'hoy':today, 'covid':turnosC, 'cantC':cantC, 'demasC':dtc, 'gripe':turnosG,'cantG':cantG,'demasG':dtg, 'fiebre':turnosF,'cantF':cantF,'demasF':dtf,'ok': response.session["ok"]})

def modificarContraseñaDeAdminDC(response):
    if not checkearLogin(response):
        return redirect('/')
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
                messages.success(response, 'Las contraseñas se ha modificado correctamente')
                return redirect('/miInfo')
    else:
        messages.warning(response, 'La contraseña actual no es correcta.')
    return redirect('/modificarContraseñaDeAdminDC')

def modCAdmin(response):
    return render(response,'modificarContraseñaAdminDC.html')
