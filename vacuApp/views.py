from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def register(response):
    return render(response,'register/register.html')

def home(response):
    return render(response,'home.html')

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

def enviarmail(request):
    exec= '../scripts/pruebaemails.py'
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")