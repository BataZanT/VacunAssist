from django.urls import path
from . import views


urlpatterns = [
    path('register',views.testBulma,name='register')
]