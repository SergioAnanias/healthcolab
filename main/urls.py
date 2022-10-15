from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.registerForm),
    path('new', views.new),
    path('logout', views.logout),
    path('logged', views.logged),
    path('home', views.home),
    path('edit', views.editForm),
    path('update', views.update)
]
