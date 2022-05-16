from django.shortcuts import render

# Create your views here.

def testBulma(response):
    return render(response,'register.html')


def home(response):
    return render(response,'home.html')

def infoPersonal(response):
    return render(response,'visualizarInfoPersonal.html')

def modificarInfo(response):
    return render(response,'modificarInfoPersonal.html')