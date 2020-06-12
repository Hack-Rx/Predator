from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexview, name='Index'),
    path('login', views.loginview, name='Login'),
    path('calorie', views.calorieview, name='Calorie')
]