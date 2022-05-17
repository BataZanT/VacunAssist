from django.urls import path
from . import views


urlpatterns = [
    path('register',views.register,name='register'),
    path('',views.home,name='home'),
    path('login',views.login,name='login'),
    path('registerCovid',views.registerCovid,name="registerCovid"),
    path('registerGripe',views.registerGripe,name="registerGripe"),
    path('registerFiebreA',views.registerFiebreA,name="registerFiebreA"),
    path('registerCentro',views.registerCentro,name="registerCentro"),
    path('enviaremail', views.enviarmail)
]