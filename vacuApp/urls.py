from django.urls import path
from . import views


urlpatterns = [
    path('register',views.testBulma,name='register'),
    path('',views.home,name='home'), 
    path('login',views.home,name='login'),
]