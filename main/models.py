# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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



class Agenda(models.Model):
    pacientes_rut = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='pacientes_rut')
    profesionales_rut = models.ForeignKey('Profesionales', models.DO_NOTHING, db_column='profesionales_RUT')  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    estado_idestado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='estado_idestado')
    status = models.IntegerField(blank=True, null=True)


class Comentarios(models.Model):
    idcomentarios = models.IntegerField(primary_key=True)
    comentarios = models.CharField(max_length=255, blank=True, null=True)
    nficha = models.ForeignKey('Ficha', models.DO_NOTHING, db_column='nficha')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)


class Estado(models.Model):
    idestado = models.AutoField(primary_key=True)
    desc_estado = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)



class Ficha(models.Model):
    nficha = models.AutoField(primary_key=True)
    profesionales_rut = models.ForeignKey('Profesionales', models.DO_NOTHING, db_column='profesionales_RUT')  # Field name made lowercase.
    pacientes_rut = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='pacientes_rut')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)


class Pacientes(models.Model):
    rut = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    apellidos = models.CharField(max_length=255, blank=True, null=True)
    fechanacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    motivoingreso = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

class Profesionales(models.Model):
    rut = models.CharField(db_column='RUT', primary_key=True, max_length=10)  # Field name made lowercase.
    nombres = models.CharField(max_length=255, blank=True, null=True)
    apellidos = models.CharField(max_length=255, blank=True, null=True)
    numregistro = models.CharField(max_length=20, blank=True, null=True)
    profesiones_idprofesiones = models.ForeignKey('Profesiones', models.DO_NOTHING, db_column='profesiones_idprofesiones')
    contrasena = models.CharField(max_length=255, blank=True, null=True)
    fechanacimiento = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    
    
    objects= ProfesionalesManager()


class Profesiones(models.Model):
    idprofesiones = models.IntegerField(primary_key=True)
    desc_profesion = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)



