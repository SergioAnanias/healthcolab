from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
import json 
from django.core import serializers
from django.forms.models import model_to_dict
from .decorators import *
from django.http import JsonResponse


def index(request):
    if not 'profesional' in request.session or not request.session['profesional']:
        return render(request, 'login.html')
    return redirect("/home")

def registerForm(request):
    context ={
        "profesiones":Profesiones.objects.all()
    }
    if not 'profesional' in request.session or not request.session['profesional']:
        return render(request, 'register.html',context)
    return redirect("/home")

def new(request):
    post_data = json.load(request)['profesional']
    print(post_data)
    errors = Profesionales.objects.validator(post_data)
        # En caso de que se devuelvan errores del validador, se guardan con messages y se redirecciona al formulario de registro para mostrarlos
    if len(errors) > 0:
        errorsarray=[]
        for k, v in errors.items():
            errorsarray.append(v)
        return JsonResponse({'errors':errorsarray}, status=500)
    pwhash = bcrypt.hashpw(post_data["password"].encode(), bcrypt.gensalt()).decode()
    profesional = Profesionales.objects.create(
        rut=post_data["rut"],
        nombres= post_data["nombres"],
        apellidos=post_data["apellidos"],
        numregistro=post_data["nregistro"],
        profesiones_idprofesiones= Profesiones.objects.get(idprofesiones=post_data["profesiones"]),
        contrasena=pwhash,
        fechanacimiento=post_data["dateborn"],
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


def register(request):
    pass

@loginauth
def logout(request):
    request.session.flush()
    return redirect("/")