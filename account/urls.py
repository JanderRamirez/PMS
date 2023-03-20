from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('login', views.login, name='welcome'),
    path('logout', views.logout, name='welcome'),
]