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
        email=post_data["email"],
        numregistro=post_data["nregistro"],
        profesiones_idprofesiones= Profesiones.objects.get(idprofesiones=post_data["profesiones"]),
        contrasena=pwhash,
        fechanacimiento=post_data["dateborn"],
        created_at=datetime.now(),
        status=1
    )
    return redirect('/')


def logged(request):
    post_data = json.load(request)['login']
    print(post_data)
    try:
        profesional = model_to_dict(Profesionales.objects.get(rut=post_data["RUT"]))
        profesional['fechanacimiento'] = profesional['fechanacimiento'].strftime('%d/%m/%Y')
        profesional['created_at'] = profesional['created_at'].strftime('%d/%m/%Y')

        if profesional['updated_at'] is not None:
            profesional['updated_at'] = profesional['updated_at'].strftime('%d/%m/%Y')
        pw=profesional["contrasena"]
        if not bcrypt.checkpw(post_data['password'].encode(), pw.encode()):
            return JsonResponse({'errors':['Datos no validos']},status=500)
        else:
            request.session["profesional"]=profesional
            return redirect('/home')
    except:
        return JsonResponse({'errors':['Datos no validos']},status=500)

@loginauth
def home(request):
    
    data = {
        'usuario':request.session['profesional']
    }
    return render(request,'index.html',data)

@loginauth
def logout(request):
    request.session.flush()
    return redirect("/")

@loginauth
def editForm(request):
    usuario = request.session['profesional']
    usuario['fechanacimiento'] = datetime.strptime(usuario['fechanacimiento'], '%d/%m/%Y').date()
    print(usuario['fechanacimiento'])
    context ={
        "profesiones":Profesiones.objects.all(),
        "usuario":usuario
    }
    return render(request, 'register.html',context)

@loginauth
def update(request):
    post_data = json.load(request)['profesional']
    current_data = request.session['profesional']
    del post_data['csrfmiddlewartetoken']
    errors = Profesionales.objects.updateValidator(post_data,current_data)
    # En caso de que se devuelvan errores del validador, se guardan con messages y se redirecciona al formulario de registro para mostrarlos
    if len(errors) > 0:
        errorsarray=[]
        for k, v in errors.items():
            errorsarray.append(v)
        return JsonResponse({'errors':errorsarray}, status=500)
    profesional = Profesionales.objects.filter(rut=current_data['rut'])
    profesionaldict = model_to_dict(profesional[0])
    if(post_data['password'] != ''):
        pwhash = bcrypt.hashpw(post_data["password"].encode(), bcrypt.gensalt()).decode()
    else:
        pwhash=profesionaldict['contrasena']
    profesional.update(
        rut= post_data['rut'],
        nombres= post_data["nombres"],
        apellidos=post_data["apellidos"],
        email=post_data["email"],
        numregistro=post_data["nregistro"],
        profesiones_idprofesiones= Profesiones.objects.get(idprofesiones=post_data["profesiones"]),
        contrasena=pwhash,
        fechanacimiento=post_data["dateborn"],
        updated_at=datetime.now(),
        status=1
    )
    profesional = model_to_dict(Profesionales.objects.get(rut=post_data['rut']))
    profesional['fechanacimiento'] = profesional['fechanacimiento'].strftime('%d/%m/%Y')
    profesional['created_at'] = profesional['created_at'].strftime('%d/%m/%Y')
    if profesional['updated_at'] is not None:
        profesional['updated_at'] = profesional['updated_at'].strftime('%d/%m/%Y')
    request.session["profesional"]=profesional
    return JsonResponse({'status':'ok'},status=200)

@loginauth
def pacientes(request):
    usuario = request.session['profesional']
    profesional = Profesionales.objects.get(rut=usuario['rut'])
    pacientes = Pacientes.objects.filter(ficha__profesionales_rut=Profesionales.objects.get(rut=profesional.rut),ficha__status=1)
    context ={
        "usuario":usuario,
        "pacientes":pacientes
    }
    return render(request, 'pacientes.html', context)




@loginauth
def nuevopaciente(request):
    usuario = request.session['profesional']
    context ={
        "usuario":usuario
    }
    return render(request, 'nuevopaciente.html', context)

def paciente(request, rut=None):
    if request.method == 'POST':
        profesional = Profesionales.objects.get(rut=request.session['profesional']['rut'])
        post_data = json.load(request)['paciente']
        errors = Pacientes.objects.validator(post_data)
        if len(errors)>0:
            errorsarray=[]
            for k, v in errors.items():
                errorsarray.append(v)
            return JsonResponse({'errors':errorsarray}, status=500)
        if len(Pacientes.objects.filter(rut=post_data["rut"])) > 0 :
            paciente = Pacientes.objects.get(rut=post_data["rut"])
            print(paciente)
        else:
            paciente = Pacientes.objects.create(
                rut=post_data["rut"],
                nombre= post_data["nombres"],
                apellidos=post_data["apellidos"],
                email=post_data["email"],
                fechanacimiento=post_data['dateborn'],
                direccion=post_data['direccion'],
                telefono=post_data['telefono'],
                created_at=datetime.now(),
                status=1
            )
        if len(Ficha.objects.filter(profesionales_rut=profesional, pacientes_rut=paciente))>0:
            ficha = Ficha.objects.filter(profesionales_rut=profesional, pacientes_rut=paciente)
            ficha.update(motivoingreso=post_data['motivoConsulta'], status=1)
            return JsonResponse({'status':'ok'},status=200)

        else:
            ficha = Ficha.objects.create(
                profesionales_rut=profesional,
                pacientes_rut=paciente,
                created_at=datetime.now(),
                motivoingreso=post_data['motivoConsulta'],
                status=1
            )
            return JsonResponse({'status':'ok'},status=200)
    elif request.method == 'DELETE':
        try:
            rutPaciente = json.load(request)['rutPaciente']
            paciente = Pacientes.objects.get(rut=rutPaciente)
            profesional = Profesionales.objects.get(rut=request.session['profesional']['rut'])
            ficha = Ficha.objects.filter(pacientes_rut=paciente, profesionales_rut=profesional)
            ficha.update(status=0)
            return JsonResponse({'status':'ok'},status=200)
        except:
            return JsonResponse({'errors':['Ha habido un error']},status=400)
    if request.method == 'GET':
        try:
            paciente = Pacientes.objects.filter(rut=rut)
            if len(paciente)>0:
                paciente = paciente.values()[0]
                return JsonResponse({'paciente':paciente}, status= 200)
            else:
                return JsonResponse({'errors':['El paciente no ha sido encontrado']},status=500)
        except:
            return JsonResponse({'errors':['Ha habido un error']},status=400)