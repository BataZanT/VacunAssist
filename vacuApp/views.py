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
    o= User.objects.all()
    idu=response.session["user_id"]
    usu=o.get(id=idu)
    edad = calculate_age(usu.birthDate)
    return render(response,'visualizarInfoPersonal.html', {"usuario":usu,"edad":edad})

def modificarInfo(response):
    if not checkearLogin(response):
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
         return redirect('http://127.0.0.1:8000/homeAdminCentro')     
    else:
        NCOMPLETO = usu.name + ' ' + usu.surname
        turnos = usu.appointment_set.all()
        fiebre_disp = False
        vacF = Vaccine.objects.get(name="Fiebre Amarilla")
        if ((usu.history.fiebreA == False)) and (calculate_age(usu.birthDate) < 60):
            if( not tieneTurno(usu,vacF)):
                fiebre_disp = True            
        return render(response,'inicioPaciente.html', {'NOMBRE': NCOMPLETO, 'turnos': turnos, 'fiebre_disp':fiebre_disp,'user':usu,'dosis':(usu.history.covid_doses + 1)})
    
def modificarContraseña(response):
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
                messages.warning(response, 'Las contraseñas se ha modificado correctamente')
                return redirect('http://127.0.0.1:8000/modificarInfo') 
    else:
        messages.warning(response, 'La contraseña actual no es correcta.')
    return redirect('http://127.0.0.1:8000/modContraseña') 
 
def asignarTurnoFiebreA(response):
    if not checkearLogin(response):
        return redirect('/')
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

def validarUsuRecuperar(response):
    mail=response.POST['mail']
    o=User.objects.all()
    usu=o.filter(email=mail).exists()
    if usu:
        token=response.POST['token']
        usu=o.get(email=mail)
        if(not usu.is_staff):
            if usu.token==token:
                response.session['email']=mail
                return mailRecuperarContraseña(response)
            else:
                messages.warning(response, 'El token no es el correcto.')
        else:
             messages.warning(response, 'Un administrador de cento no puede cambiar su contraseña, comuniquese con su superior.')   
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
    o= User.objects.all()
    idUsuario = response.session["user_id"]
    usu = o.get(id = idUsuario)
    NCOMPLETO = usu.name + ' ' + usu.surname
    messages.success(response, ' Bienvenid@ a VacunAssist '+NCOMPLETO)
    t=Appointment.objects.all()
    today = date.today()
    #covid
    turnosC=t.filter(vaccine=1,state=1,center=usu.center,date=today)
    dtc=t.filter(vaccine=1,center=usu.center,date=today).exclude(state=1)
    print (dtc)
    if (not dtc):
        dtc=0
    if (not turnosC):
        turnosC=0
        cantC=0
    else:
        cantC=t.filter(vaccine=1,state=1,center=usu.center,date=today).count()
    #gripe
    turnosG=t.filter(vaccine=2,state=1,center=usu.center,date=today)
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
        print (dni)
        o=User.objects.all()
        u=o.filter(DNI=dni).exists()
        print(u)
        if (u):
            u=o.get(DNI=dni)
            today = date.today()
            a=o.get(id=response.session["user_id"])
            centro=a.center
            t=u.appointment_set.filter(state=1,date=today,center=centro).exists()
            if(t):
                t=u.appointment_set.get(state=1,date=today,center=centro)
                usubuscado=t 
            else:
                usubuscado=1
        else:
            usubuscado=2
    return render(response,'inicioAdminCentro.html', {'turnobuscado':usubuscado,'tot':tot,'hoy':today, 'covid':turnosC, 'cantC':cantC, 'demasC':dtc, 'gripe':turnosG,'cantG':cantG,'demasG':dtg, 'fiebre':turnosF,'cantF':cantF,'demasF':dtf,'ok': response.session["ok"]})

def presente(response,id,tipo):
    if not checkearLogin(response):
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
            usu.appointment_set.create(state=0,center=usu.center,vaccine=vacC)
    else:
        if (tipo == 2):
            historialActual.gripe_date = datetime.today().strftime('%Y-%m-%d')
        else:     
            historialActual.fiebreA_date = datetime.today().strftime('%Y-%m-%d')
            
    turnoActual.save()
    historialActual.save()                
    return redirect('http://127.0.0.1:8000/homeAdminCentro')

def marcarTurnoAusentes(response):
        if not checkearLogin(response):
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
                        turno.save()
                else:
                    messages.error(response,"No hay turnos para marcar como ausentes")
            response.session["ok"]=0
        return redirect('http://127.0.0.1:8000/homeAdminCentro')

def pasarAadminiReiniciarbuscarUsuario(response):
    response.session["dni"]=response.POST["dni"]
    if (response.session["usubuscar"]==0):
        response.session["usubuscar"]=1
    return redirect('http://127.0.0.1:8000/homeAdminCentro')

def checkearLogin(response):
    return "user_id" in response.session
        
def informacionVacunas(response):
    return render(response,'infoVacunas.html')

def completarVacunas(response,id,tipo):
    T = Appointment.objects.all()
    turnoActual = T.get(id = id)
    usu = User.objects.get(id = turnoActual.patient_id)
    NCOMPLETO = usu.name + ' ' + usu.surname
    return render(response,'completarTurnoVacuna.html', {'idApp':id,'tipoVacuna':tipo, 'nombre': NCOMPLETO})

def seleccionarCentro(response):
    centros = Center.objects.all()
    return render(response,'seleccionarCentro.html', {'todosLosCentros': centros})

def modificarCentro(response, id):
    return render(response,'ingresarNuevaInfo.html', {'centro':id})

def modificar(response, id):
    nombreNuevo = response.POST["nombre"]
    direccNueva = response.POST["direccion"]
    c = Center.objects.get(id = id)
    if (nombreNuevo == "") and (direccNueva == ""):
            messages.info(response,'No hay informacion nueva que cargar')
    else:     
        if (nombreNuevo != ""):
            if (c.name == nombreNuevo):
                messages.error(response,'El nombre no puede ser el actual')
                return render(response,'ingresarNuevaInfo.html', {'centro':id}) 
            else:
                todosLosCentros = Center.objects.all()
                cCopiado = todosLosCentros.filter(name = nombreNuevo)    
                if cCopiado:
                    messages.warning(response, 'El nombre nuevo coincide con el de otro centro')
                    return render(response,'ingresarNuevaInfo.html', {'centro':id})
                else:
                    messages.success(response,'Nombre modificado con exito')
                    c.name = nombreNuevo
        if (direccNueva != ""):
            if (c.adress == direccNueva):
                messages.error(response,'La direccion nueva no puede ser la actual')
                return render(response,'ingresarNuevaInfo.html', {'centro':id}) 
            else:
                todosLosCentros = Center.objects.all()
                cCopiado = todosLosCentros.filter(adress = direccNueva)    
                if cCopiado:
                    messages.warning(response, 'La direccion nueva coincide con la de otro centro')
                    return render(response,'ingresarNuevaInfo.html', {'centro':id})
                else:
                    messages.success(response,'Direccion modificada con exito')
                    c.adress = direccNueva
        c.save()
    centros = Center.objects.all()
    return render(response,'seleccionarCentro.html', {'todosLosCentros': centros})

def crearCentro(response):
    return render(response,'crearCentro.html')

def crearCentroNuevo(response):
    nombreNuevo = response.POST["nombre"]
    direccNueva = response.POST["direccion"]  
    todosLosCentros = Center.objects.all()
    cCopiado = todosLosCentros.filter(name = nombreNuevo)    
    if cCopiado:
        messages.warning(response, 'El nombre nuevo coincide con el de otro centro')
        return render(response,'crearCentro.html')
    cCopiado = todosLosCentros.filter(adress = direccNueva)    
    if cCopiado:
        messages.warning(response, 'La direccion nueva coincide con la de otro centro')
        return render(response,'crearCentro.html')
    c = Center(name=nombreNuevo,adress=direccNueva, id= (Center.objects.count()) + 1)
    c.save()
    return render(response,'seleccionarCentro.html', {'todosLosCentros': todosLosCentros})

def enviaremail(response, admin): 
    
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
        body = 'Este es un mensage autogenerado por VacunAssist. Para acceder a su cuenta utilice la siguiente clave ' + str(admin.password) + ',su TOKEN es ' + str(TOKEN)          
        msg = f'Subject: {subject}\n\n{body}'                                       #Es necesario formatear el mensaje (f) para que lo tome gmail
        smtp.sendmail(EMAIL, DESTINATARIO, msg)                                     #Para enviarlo usamos sendmail con quien lo envia, a quien y el mensaje en cuestion
    response.session.flush()
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def crearAdmin(response):
    centros = Center.objects.all()
    return render(response,'crearAdmin.html', {'todosLosCentros': centros})
    
def completarAdmin(response):
    nombreNuevo = response.POST["nombre"]
    apellidoNuevo = response.POST["apellido"]
    emailNuevo = response.POST["email"]
    o= User.objects.all()
    usu = o.filter(email=emailNuevo)
    if usu:
        messages.error(response, 'El mail pertenece a otra cuenta del sistema')
        centros = Center.objects.all()
        return render(response,'crearAdmin.html', {'todosLosCentros': centros})   
    else:
        c = Center.objects.get(id = response.POST.get('elegido'))
        adminNuevo = User(id= (User.objects.count() + 1), name= nombreNuevo, surname= apellidoNuevo, email= emailNuevo, birthDate= '2000-06-05', DNI= (11111111 + (random.randint(1000, 9999))), center_id= c.id, is_staff= True, is_admin=False)
        CLAVE = str(random.randint( 1000000, 9999999)) + str("V")
        adminNuevo.set_password(CLAVE)
        print (CLAVE)
        adminNuevo.save()
        enviaremail(response, adminNuevo)
        messages.success(response, 'Se ha creado un nuevo administrador de centro')
        return render(response,'home.html')
    
def testPandas(response):
    centros = Center.objects.all()
    turnos = Appointment.objects.all()
    cantidades = []
    Ncentros = []
    for centro in centros:
        cant = turnos.filter(center = centro).count()
        cantidades.append(cant)
        Ncentros.append(centro.name)
    return render(response,'testPandas.html',{'df':Ncentros,'df1':cantidades})

def turnosAsignados(response,pagina = 1,filtro='centro'):
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

def turnosParaAsignar(response,pagina = 1,filtro='centro'):
    turnos = Appointment.objects.filter(state = 0)
    fecha = None
    if response.method == "POST":
        fecha = response.POST["fecha"]
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
    return render(response,'turnosParaAsignar.html',{'pagina':pagina_actual,'paginas':p,'fecha':fecha})

def asignarTurnos(response,fecha):
    turnos = response.POST.getlist("turnos[]")
    print(turnos)
    for turno in turnos:
        turnobj = Appointment.objects.get(id = turno)
        turnobj.state = 1
        turnobj.date = fecha
        turnobj.save()
    turnos = Appointment.objects.filter(state = 0)
    p = Paginator(turnos,12)
    fecha = None
    return render(response,'turnosParaAsignar.html',{'pagina':p.page(1),'paginas':p,'fecha':fecha})
        






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

def elegir(response):
    return render(response,'elegirOpcion.html')

def seleccionarAdministrador(response):
    a = User.objects.filter(is_staff = 1)
    return render(response,'seleccionarAdministrador.html',{'todosLosAdmins':a})

def borrarAdmin(response):
    a = User.objects.filter(is_staff = 1)
    return render(response,'borrarAdminX.html',{'todosLosAdmins':a})
