from django.shortcuts import render

# Create your views here.

def register(response):
    return render(response,'register.html')


def home(response):
    return render(response,'home.html')

def registerCovid(response):
    return render(response,'registerCovid.html')

def registerGripe(response):
    return render(response,'registerGripe.html')