from . import views
from .models import User
from datetime import date,datetime

def validarRegister(data):
    message = ''
    o = User.objects
    if( not (data["name"].isalpha())):
        message = 'El nombre solo puede contener letras'
    elif(not (data["surname"].isalpha())):
        message = 'El apellido solo puede contener letras'
    elif(o.filter(email= data["email"]).exists()):
        message = 'El email ya esta en uso'
    elif(o.filter(DNI= data["DNI"]).exists()):
        message = 'El DNI ya tiene un usuario asignado'
    elif(data["birthDate"] > date.today()):
        message = 'La fecha de nacimiento no puede ser mayor que la fecha de hoy'
   
    elif(not (data["password1"] == data["password2"])):
        message = 'Las contraseñas no coinciden'
    
    elif(len(data["password1"]) < 8 ):
        message = 'La contraseña debe contener al menos 8 caracteres'
    else:
        upper = False
        for character in data["password1"]:
            if character.isupper():
                    upper = True
        if(not upper):
            message = 'La contraseña debe contener al menos una letra mayuscula'
    return message


def validarCovid(data):
    message = ''
    if(int(data["covid"]) > 0):
        if (data['covid_date'] is None):
            message = 'Es necesario agregar la fecha de la ultima dosis'
    
    return message 

def validarFiebreA(data):
    message = ''
    if(int(data["fiebreA"]) == 1):
        if (data['fiebreA_date'] is None):
            message = 'Es necesario agregar la fecha de vacunacion'
    return message

def validarGripe(data):
    message = ''
    if(int(data["gripe"]) == 1):
        if (data['gripe_date'] is None):
            message = 'Es necesario agregar la fecha de vacunacion'
    return message

