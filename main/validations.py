from django.db import models
import re
import bcrypt
from datetime import datetime, date

class ProfesionalesManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData["rut"]) == 0:
            errors["rut"] = "El campo rut se encuentra vacio"
        elif len(postData["rut"])>0:
            #Valida el rut
            RUT_REGEX=re.compile(r'^(\d{1,2})(\d{3})(\d{3})-(\w{1})$')
            if not re.match(RUT_REGEX, postData["rut"]):
                errors["rut"]="RUT no valido"
            exists = super().get_queryset().filter(rut=postData["rut"])
            if(len(exists)>=1): 
                errors["rut"]="El rut ya existe"
        if len(postData["nombres"]) == 0:
            errors["nombres"] = "El campo nombre se encuentra vacio"
        if len(postData["apellidos"]) == 0:
            errors["apellidos"] = "El campo apellidos se encuentra vacio"
        if len(postData["email"])>0:
            EMAIL_REGEX=re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')
            # Valida si el email sigue una expresión regular
            if not re.match(EMAIL_REGEX, postData["email"]):
                errors["email"]="Email no valido"
            # Valida si el correo existe o no
                if len(Profesionales.objects.filter(email=postData["email"])) > 0:
                    errors["exists"]= "El correo ya existe"
        # Valida la longitud de la contraseña
        if len(postData["password"]) == 0 or len(postData["password"]) < 5:
            errors["passwordlen"]= "La contraseña debe tener al menos 5 caracteres"
        #Valida si las constraseñas coinciden
        elif postData["password"] != postData["cpassword"]:
            errors["password"] = "Las contraseñas no coinciden"
        #Valida si la fecha no esta nula, es una fecha valida, y ademas si es que la fecha esta en pasado
        if len(postData["dateborn"]) == 0 or len(postData["dateborn"]) < 10 or datetime.strptime(postData["dateborn"], "%Y-%m-%d") > datetime.now(): 
            errors["age"] = "Debe ingresar una fecha de nacimiento valida"
        if len(postData["nregistro"])>0:
            NREGISTRO_REGEX = re.compile(r'^[0-9]{1,6}$')
            if not re.match(NREGISTRO_REGEX, postData["nregistro"]):
                errors["nregistro"] = "Numero de registro no es valido"
        elif len(postData)==0:
            errors["nregistro"] = "Debe ingresar un numero de registro"
        return errors


    def loginvalidator(self, postData):
        errors={}
        if len(Profesionales.objects.filter(rut=postData["rut"])) == 0:
            errors['notfound']= "Not valid login"
        else:
            pw1= User.objects.get(email=postData["email"]).password
            if not bcrypt.checkpw(postData['password'].encode(), pw1.encode()):
                errors['password']="Not valid login"
        return errors

    def updateValidator(self, postData, current_data):
        errors={}
        if(postData["rut"] != current_data['rut']):
            if len(postData["rut"]) == 0:
                errors["rut"] = "El campo rut se encuentra vacio"
            elif len(postData["rut"])>0:
                #Valida el rut
                RUT_REGEX=re.compile(r'^(\d{1,2})(\d{3})(\d{3})-(\w{1})$')
                if not re.match(RUT_REGEX, postData["rut"]):
                    errors["rut"]="RUT no valido"
                exists = super().get_queryset().filter(rut=postData["rut"])
                if(postData['rut'] !=current_data['rut'] and  len(exists)>=1): 
                    errors["rut"]="El rut ya existe"
        if len(postData["nombres"]) == 0:
            errors["nombres"] = "El campo nombre se encuentra vacio"
        if len(postData["apellidos"]) == 0:
            errors["apellidos"] = "El campo apellidos se encuentra vacio"
        if len(postData["email"])>0:
            EMAIL_REGEX=re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')
            # Valida si el email sigue una expresión regular
            if not re.match(EMAIL_REGEX, postData["email"]):
                errors["email"]="Email no valido"
            # Valida si el correo existe o no
                if len(Profesionales.objects.filter(email=postData["email"])) > 0:
                    errors["exists"]= "El correo ya existe"
        # Valida la longitud de la contraseña
        if postData["password"] != '':
            if len(postData["password"]) < 5:
                errors["passwordlen"]= "La contraseña debe tener al menos 5 caracteres"
            #Valida si las constraseñas coinciden
            elif postData["password"] != postData["cpassword"]:
                errors["password"] = "Las contraseñas no coinciden"
            #Valida si la fecha no esta nula, es una fecha valida, y ademas si es que la fecha esta en pasado
        if len(postData["dateborn"]) == 0 or len(postData["dateborn"]) < 10 or datetime.strptime(postData["dateborn"], "%Y-%m-%d") > datetime.now(): 
            errors["age"] = "Debe ingresar una fecha de nacimiento valida"
        if len(postData["nregistro"])>0:
            NREGISTRO_REGEX = re.compile(r'^[0-9]{1,6}$')
            if not re.match(NREGISTRO_REGEX, postData["nregistro"]):
                errors["nregistro"] = "Numero de registro no es valido"
        elif len(postData)==0:
            errors["nregistro"] = "Debe ingresar un numero de registro"
        return errors


class PacientesManager(models.Manager):
    def validator(self, post_data):
        errors={}
        if len(post_data["rut"]) == 0:
            errors["rut"] = "El campo rut se encuentra vacio"
        elif len(post_data["rut"])>0:
            #Valida el rut
            RUT_REGEX=re.compile(r'^(\d{1,2})(\d{3})(\d{3})-(\w{1})$')
            if not re.match(RUT_REGEX, post_data["rut"]):
                errors["rut"]="RUT no valido"
        if len(post_data["nombres"]) == 0:
            errors["nombres"] = "El campo nombre se encuentra vacio"
        if len(post_data["apellidos"]) == 0:
            errors["apellidos"] = "El campo apellidos se encuentra vacio"
        if len(post_data["email"])>0:
            EMAIL_REGEX=re.compile(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+')
            # Valida si el email sigue una expresión regular
            if not re.match(EMAIL_REGEX, post_data["email"]):
                errors["email"]="Email no valido"
            # Valida si el correo existe o no
        #Valida si la fecha no esta nula, es una fecha valida, y ademas si es que la fecha esta en pasado
        if len(post_data["dateborn"]) == 0 or len(post_data["dateborn"]) < 10 or datetime.strptime(post_data["dateborn"], "%Y-%m-%d") > datetime.now(): 
            errors["age"] = "Debe ingresar una fecha de nacimiento valida"
        if len(post_data["telefono"]) == 0:
            errors["telefono"] = "El campo telefono se encuentra vacio"
        if len(post_data["direccion"]) == 0:
            errors["direccion"] = "El campo direccion se encuentra vacio"
        if len(post_data["motivoConsulta"]) == 0:
            errors["motivoConsulta"] = "El campo motivo de consulta se encuentra vacio"
        print(post_data)
        return errors


class AgendaManager(models.Manager):
    def validator(self,post_data):
        errors={}
        if datetime.strptime(post_data['fecha']+" "+ post_data['hora'], "%Y-%m-%d %H:%M") < datetime.now():
            errors['fechainvalida']="La fecha ingresada no es valida"
        return errors