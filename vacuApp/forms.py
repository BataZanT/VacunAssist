
from django import forms
class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
                'id': 'loginEmail',
                'type': 'text',
                'class': 'form-control'
            })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'loginPassword',
            'type': 'password',
            'class': 'form-control',
        })
       )
    token = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'loginToken',
            'type': 'text',
            'class': 'form-control'
         })
    )
 
from django import forms
from django.forms import CharField
class Register(forms.Form):
    name = CharField(label="Nombre", max_length="50")
    surname = CharField(label="Apellido",max_length=90)
    email = forms.EmailField()
    DNI = forms.IntegerField(label="DNI",max_value=99999999,min_value=1000000)
    birthDate = forms.DateField(label="Fecha de Nacimiento")
    SEX = [
        ('F','F'),
        ('M','M')
    ]
    sex = forms.ChoiceField(label="Sexo",choices = SEX,)
    password = CharField(label="Contraseña",max_length=10)
    repeatPassword = CharField(label="Repetir Contraseña",max_length=10,widget= forms.TextInput
                           (attrs={'type':'password'}))
