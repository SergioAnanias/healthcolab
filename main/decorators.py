from django.shortcuts import render, HttpResponse, redirect
def loginauth(func):
    def wrapper(request):
        if not 'profesional' in request.session or not request.session['profesional']:
            return redirect("/")
        return func(request)
    return wrapper


def loginauthPaciente(func):
    def wrapper(request, rut=None):
        if not 'profesional' in request.session or not request.session['profesional']:
            return redirect("/")
        return func(request, rut)
    return wrapper


def loginauthAll(func):
    def wrapper(request,rutPaciente=None,rutProfesional=None):
        if not 'profesional' in request.session or not request.session['profesional']:
            return redirect("/")
        return func(request,rutPaciente,rutProfesional)
    return wrapper