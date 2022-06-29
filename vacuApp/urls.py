from django.urls import path
from . import views
from .views import  PdfCovid, PdfFiebreA, PdfGripe

urlpatterns = [
    path('infoPersonal',views.infoPersonal,name='visualizarInfoPersonal'),
    path('modificarInfo',views.modificarInfo,name='modificarInfoPersonal'),
    path('modContraseña',views.modContraseña,name='modificarContraseña'),
    path('modMail',views.modMail,name='modificarMail'),
    path('recuContraseña',views.recuContraseña,name='recuperarContraseña'),
    path('camcontrecu',views.camContraseñaRecu,name='cambiarContraseñaRecuperada'),
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
    path('validarRecu',views.validarUsuRecuperar),
    path('modContRecup',views.validarCambioContraseñaRecuperada),
    path('validarMail',views.validarCambioMail),    
    path('modCentro',views.modCentro),  
    path('certifFiebreA', PdfFiebreA.as_view()),
    path('certifCovid', PdfCovid.as_view()),
    path('certifGripe', PdfGripe.as_view()),
    path('certifGripe', PdfGripe.as_view()),
    path('elegirCertificado',views.elegirCertificado),
    path('validarCambioCentro',views.validarCambioCentro), 
    path('cancelarRegistro',views.borrarRegistro),
    path('homeAdminCentro',views.homeAdmin),  
    path('pasarPresente/<int:id>/<int:tipo>',views.presente),         
    path('ausentes',views.marcarTurnoAusentes),
    path('buscar',views.pasarAadminiReiniciarbuscarUsuario),
    path('infoVacunas',views.informacionVacunas),
    path('completarTurno/<int:id>/<int:tipo>',views.completarVacunas),
    path('testPandas',views.testPandas),
    path('turnosAsignados',views.turnosAsignados),
    path('envioMailRecuperar',views.verEnvioMailRecuperar)
]
