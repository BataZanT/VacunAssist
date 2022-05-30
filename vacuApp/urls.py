from django.urls import path
from . import views

urlpatterns = [
    path('infoPersonal',views.infoPersonal,name='visualizarInfoPersonal'),
    path('modificarInfo',views.modificarInfo,name='modificarInfoPersonal'),
    path('modContraseña',views.modContraseña,name='modificarContraseña'),
    path('modMail',views.modMail,name='modificarMail'),
    path('recuContraseña',views.recuContraseña,name='recuperarContraseña'),
    path('camContraseñaRecu',views.camContraseñaRecu,name='cambiarContraseñaRecuperada'),
    path('register',views.register,name='register'),
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('registerCovid',views.registerCovid,name="registerCovid"),
    path('registerGripe',views.registerGripe,name="registerGripe"),
    path('registerFiebreA',views.registerFiebreA,name="registerFiebreA"),
    path('registerCentro',views.registerCentro,name="registerCentro"),
    path('enviaremail', views.enviaremail),
    path('validar',views.validar),
    path('cerrarSesion',views.CerrarSesion),
    path('homeUsuario',views.homeUsuario),
    path('validarContraseñaAModificar',views.modificarContraseña),
    path('turnoFiebreA',views.asignarTurnoFiebreA),
    path('validarMail',views.validarCambioMail),    
    path('modCentro',views.modCentro),  
    path('validarCambioCentro',views.validarCambioCentro), 
    path('cancelarRegistro',views.borrarRegistro),       
]

