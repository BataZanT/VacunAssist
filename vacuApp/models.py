from xmlrpc.client import Boolean
from django.db import models
from django.db.models import CharField
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


##ESTO SIRVE PARA QUE DJANGO MANEJE PIOLA A NUESTRO USER
class MyUserManager(BaseUserManager):
        def create_user(self, name, surname, email, DNI, birthDate, sex, password, token=None, Center=None):
            
            if not email:
                raise ValueError('Users must have an email address')

            user = self.model(
                name=name,
                surname=surname,
                email=self.normalize_email(email),
                DNI = DNI,
                birthDate = birthDate,
                sex = sex,
                password = password,   
            )
            user.set_password(password)
            user.save(using=self._db)
            return user


# Create your models here.


class Center(models.Model):
    name = CharField(max_length=100)
    adress = CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class User(AbstractBaseUser):
    name = CharField(max_length=50)
    surname = CharField(max_length=90)
    email = CharField(max_length=100,unique=True)
    DNI = CharField(max_length=8, unique=True)
    birthDate = models.DateField()
    sex = CharField(max_length=1)
    password = CharField(max_length=20)
    token = CharField(max_length=4, null=True,default='1111')
    center = models.ForeignKey(Center, null=True,on_delete=models.CASCADE)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    @property
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    


    
    def __str__(self):
        return str(self.name + ' ' + self.surname + ' ' + self.DNI)
    


class Vaccine(models.Model):
    name = CharField(max_length=40)

    def __str__(self):
        return str(self.name)


class Appointment(models.Model):
    state = models.IntegerField() # 0 es pendiente, 1 es asignado, 2 es completado. Cuando se cancela se vuelve a pendiente 
    date = models.DateField(null = True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(str(self.vaccine) + ' ' + str(self.patient) + ' ' + str(self.state))

class History(models.Model):
    covid_doses = models.IntegerField()
    covid_date = models.DateField(null=True)
    gripe = models.BooleanField()
    gripe_date = models.DateField(null=True)
    fiebreA = models.BooleanField()
    fiebreA_date = models.DateField(null=True)
    fiebreA_eleccion = models.BooleanField()
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )

    
