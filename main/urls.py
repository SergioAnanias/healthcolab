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
    path('update', views.update),
    path('pacientes', views.pacientes),
    path('nuevopaciente', views.nuevopaciente),
    path('paciente/<str:rut>', views.paciente),
    path('profesional_has_paciente/<str:rutPaciente>/<str:rutProfesional>', views.profesional_has_paciente),
    path('paciente', views.paciente),
    path('agenda', views.agenda),
    path('submit_agendamiento', views.submit_agendamiento),
    path('update_agendamiento', views.update_agendamiento),
    path('edit_paciente/<str:rutPaciente>',views.edit_paciente),
    path('historico/',views.historico),
    path('ficha/<str:rutPaciente>',views.ficha_paciente)
]
