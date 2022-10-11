from django.shortcuts import render, HttpResponse, redirect
def loginauth(func):
    def wrapper(request):
        if not 'profesional' in request.session or not request.session['profesional']:
            return redirect("/")
        return func(request)
    return wrapper