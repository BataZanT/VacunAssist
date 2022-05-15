from django.db import models
from django.db.models import CharField


# Create your models here.

class Center(models.Model):
    name = CharField(max_length=100)
    adress = CharField(max_length=100)

    def __str__(self):
        return str(self.name)

class User(models.Model):
    name = CharField(max_length=50)
    surname = CharField(max_length=90)
    email = CharField(max_length=100)
    DNI = CharField(max_length=8,unique=True)
    birthDate = models.DateField
    sex = CharField(max_length=1)
    password = CharField(max_length=20)
    token = CharField(max_length=4,null=True)
    center = models.ForeignKey(Center,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name + ' ' + self.surname + ' ' + self.DNI)

class Vaccine(models.Model):
    name = CharField(max_length=40)

    def __str__(self):
        return str(self.name)


class Appointment(models.Model):
    state = models.IntegerField
    date = models.DateField
    center = models.ForeignKey(Center,on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine,on_delete=models.CASCADE)
    patient = models.ForeignKey(User,on_delete=models.CASCADE)


