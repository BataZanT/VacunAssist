from django.urls import path
from . import views


urlpatterns = [
    path('register',views.testBulma,name='register'),
    path('',views.home,name='home'),
    path('infoPersonal',views.infoPersonal,name='visualizarInfoPersonal'),
    path('modificarInfo',views.modificarInfo,name='modificarInfoPersonal'),
    path('modContraseña',views.modContraseña,name='modificarContraseña'),
]