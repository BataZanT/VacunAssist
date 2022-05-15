from django.shortcuts import render

# Create your views here.

def testBulma(response):
    return render(response,'register.html')


def home(response):
    return render(response,'home.html')
