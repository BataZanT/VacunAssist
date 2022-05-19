from random import choices
from django import forms
from django.forms import CharField
class Register(forms.Form):
    name = CharField(label="Nombre", max_length="50")
    surname = CharField(label="Apellido",max_length=90)
    email = forms.EmailField()
    DNI = forms.IntegerField(label="DNI",max_value=99999999,min_value=1000000)
    birthDate = forms.DateField(label="Fecha de Nacimiento",widget= forms.DateInput())
    SEX = [
        ('F','F'),
        ('M','M')
    ]
    sex = forms.ChoiceField(label="Sexo",choices = SEX)
    password = CharField(label="Contraseña",max_length=10,widget= forms.TextInput
                           (attrs={'type':'password'}))
    repeatPassword = CharField(label="Repetir Contraseña",max_length=10,widget= forms.TextInput
                           (attrs={'type':'password'}))


class RegisterCovid(forms.Form):
    DOSIS = [
        ('1','Una dosis'),
        ('2','Dos dosis'),
        ('0','Ninguna')
    ]
    covid_date = forms.DateField(label="Cuando se aplico la ultima dosis?",widget= forms.TextInput
                           (attrs={'type':'date'}),required=False)
    covid = forms.ChoiceField(label="Cuantas dosis se ha aplicado?",choices = DOSIS,initial=2)