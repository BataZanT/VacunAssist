import logging
from django.contrib.auth import authenticate

def validar(request):
    usuario= request.POST ['usu']
    contraseña= request.POST ['con']
    user= authenticate(usuario,contraseña)
    if user!=None:
        if user.is_active:
        logging(user)
