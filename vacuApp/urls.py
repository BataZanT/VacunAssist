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
    path('envioMailRecuperar',views.verEnvioMailRecuperar),
    path('modificarCentro/<int:id>',views.modificarCentro),
    path('modificarCentroX/<int:id>',views.modificar),
    path('crearAdmin',views.crearAdmin),
    path('completarAdmin',views.completarAdmin),
    path('graficoUsuarios',views.graficoUsuarios),
    path('elegirGrafico',views.elegirGrafico),
    path('graficoCentros',views.graficoCentros),
    path('graficoVacunas',views.graficoVacunas),
    path('turnosAsignados/<filtro>/<pagina>',views.turnosAsignados),
    path('turnosAsignados/',views.turnosAsignados),
    path('turnosParaAsignar/<filtro>/<pagina>/',views.turnosParaAsignar),
    path('turnosParaAsignar/',views.turnosParaAsignar),
    path('asignarTurnos/<fecha>/<pagina>/<filtro>',views.asignarTurnos),
    path('cancelarTurno/',views.cancelarTurno),
    path('envioMailRecuperar',views.verEnvioMailRecuperar),
    path('borrarAdmin',views.borrarAdmin),
    path('seleccionarAdministracion',views.selec),
    path('modificarInfoDeAdmin/<int:id>',views.modificarAdminC), 
    path('modificarInfoDeAdminX/<int:id>',views.modificarAdminX), 
    path('preguntar/<int:id>',views.confirmarEliminar), 
    path('eliminarAdmin/<int:id>',views.eliminarAdmin),
    path('miInfo',views.miInfo),
    path('modificarMiInfo',views.modificarMiInfo),
    path('modificarContraseñaDeAdminDC',views.modCAdmin), 
    path('validarModificacion',views.modificarContraseñaDeAdminDC), 
]
