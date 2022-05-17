from django.contrib import admin
from .models import User
from .models import Center
from .models import Vaccine
from .models import Appointment
# Register your models here.
admin.site.register(User)
admin.site.register(Center)
admin.site.register(Vaccine)
admin.site.register(Appointment)