from .models import Center
from django import forms
class UserLoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(label="contraseña",min_length=8)
    token=forms.CharField(label="token",max_length=4)

 
from random import choices
from django import forms
from django.forms import CharField

class Register(forms.Form):
    name = CharField(label="Nombre", max_length=50)
    surname = CharField(label="Apellido",max_length=90)
    email = forms.EmailField()
    DNI = forms.IntegerField(label="DNI",max_value=99999999,min_value=1000000)
    birthDate = forms.DateField(label="Fecha de Nacimiento",widget= forms.DateInput())
    SEX = [
        ('F','F'),
        ('M','M')
    ]
    sex = forms.ChoiceField(label="Sexo",choices = SEX)
    password = CharField(label="Contraseña",min_length=8,max_length=10,widget= forms.TextInput
                           (attrs={'type':'password'}))
    repeatPassword = CharField(label="Repetir Contraseña",min_length=8,max_length=10,widget= forms.TextInput
                           (attrs={'type':'password'}))

class RegisterCovid(forms.Form):
    DOSIS = [
        ('1','Una dosis'),
        ('2','Dos dosis'),
        ('0','Ninguna')
    ]
    covid = forms.ChoiceField(label="¿Cuantas dosis cotra el covid-19 se ha aplicado?",choices = DOSIS,widget=forms.RadioSelect)
    covid_date = forms.DateField(label="Si se ha dado alguna ¿Cuando se aplico la ultima dosis?",widget= forms.TextInput
                           (attrs={'type':'date'}),required=False)
    
class RegisterGripe(forms.Form):
    APLICADA = [
        ('1','Si'),
        ('0','No'),
    ]
    gripe = forms.ChoiceField(label="¿Se ha aplicado la vacuna contra la gripe?", widget=forms.RadioSelect,choices = APLICADA)
    gripe_date = forms.DateField(label="¿Cuando se aplico la vacuna?",widget= forms.TextInput
                           (attrs={'type':'date'}),required=False)

class RegisterFiebreA(forms.Form):
    APLICADA = [
        ('1','Si'),
        ('0','No'),
    ]
    fiebreA = forms.ChoiceField(label="¿Se ha aplicado la vacuna contra la fiebre Amarilla?", widget=forms.RadioSelect,choices = APLICADA)
    fiebreA_date = forms.DateField(label="Si se la ha dado ¿Cuando se aplico la vacuna?",widget= forms.TextInput
                           (attrs={'type':'date'}),required=False)

class RegisterCentro(forms.Form):
    CENTROS = []
    for c in Center.objects.all():
        CENTROS.append((c.id,c.name))
            
    center = forms.ChoiceField(label="¿Cual centro desea seleccionar para que le lleguen sus turnos?", widget=forms.RadioSelect,choices = CENTROS)