from django import forms
from django.contrib import admin
from .models import User,Center,Vaccine,Appointment
from django.forms import CharField,ModelForm
# Register your models here.
admin.site.register(User)
admin.site.register(Center)
admin.site.register(Vaccine)
admin.site.register(Appointment)

class UserCreationForm(ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    name = CharField(label="Nombre", max_length="50")
    surname = CharField(label="Apellido",max_length=90)
    email = forms.EmailField()
    DNI = forms.IntegerField(label="DNI",max_value=99999999,min_value=1000000)
    birthDate = forms.DateField(label="Fecha de Nacimiento",widget= forms.TextInput
                           (attrs={'type':'date'}))
    SEX = [
        ('F','F'),
        ('M','M')
    ]
    sex = forms.ChoiceField(label="Sexo",choices = SEX,)
    password1 = CharField(label="Contraseña",max_length=10,widget= forms.PasswordInput)
    password2 = CharField(label="Repetir Contraseña",max_length=10,widget= forms.PasswordInput)


    class Meta:
        model = User
        fields = ('name','surname','email','DNI', 'birthDate','sex','password1','password2')
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

