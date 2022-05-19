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
    token = CharField(max_length=4, null=True)
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin 
    
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
    state = models.IntegerField()
    date = models.DateField()
    center = models.ForeignKey(Center, on_delete=models.CASCADE, null=True)
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)


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
        primary_key=True,
    )

    
