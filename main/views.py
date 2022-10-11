from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
import json 
from django.core import serializers
from django.forms.models import model_to_dict
from .decorators import *


def index(request):
    if 'profesional' in request.session or request.session['profesional']:
        return redirect("/home")
    return render(request, 'login.html')

def registerForm(request):
    if 'profesional' in request.session or request.session['profesional']:          
        return redirect("/home")
    context ={
        "profesiones":Profesiones.objects.all()
    }
    return render(request, 'register.html', context)

def new(request):
    print(request.POST)
    errors = Profesionales.objects.validator(request.POST)
        # En caso de que se devuelvan errores del validador, se guardan con messages y se redirecciona al formulario de registro para mostrarlos
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect("/register")
    pwhash = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()
    profesional = Profesionales.objects.create(
        rut=request.POST["rut"],
        nombres= request.POST["nombres"],
        apellidos=request.POST["apellidos"],
        numregistro=request.POST["nregistro"],
        profesiones_idprofesiones= Profesiones.objects.get(idprofesiones=request.POST["profesiones"]),
        contrasena=pwhash,
        fechanacimiento=request.POST["dateborn"],
        created_at=datetime.now(),
        status=1
    )
    return redirect('/')


def logged(request):
    try:
        profesional = model_to_dict(Profesionales.objects.get(rut=request.POST["RUT"]))
        profesional['fechanacimiento'] = profesional['fechanacimiento'].strftime('%d/%m/%Y')
        profesional['created_at'] = profesional['created_at'].strftime('%d/%m/%Y')
        if profesional['updated_at'] is not None:
            profesional['updated_at'] = profesional['update_at'].strftime('%d/%m/%Y')
        pw=profesional["contrasena"]

        if not bcrypt.checkpw(request.POST['password'].encode(), pw.encode()):
            messages.error(request, 'Datos no validos')
        else:
            request.session["profesional"]=profesional
            print(request.session["profesional"])
            return redirect("/home")

    except:
        messages.error(request, 'Datos no validos')
    
    return redirect("/")
@loginauth
def home(request):
    print(request.session['profesional'])
    data = {
        'usuario':request.session['profesional']
    }
    return render(request,'index.html',data)

def login(request):
    pass

def register(request):
    pass

@loginauth
def logout(request):
    request.session.flush()
    return redirect("/")