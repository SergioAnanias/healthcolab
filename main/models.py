# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from .validations import * 

class Agenda(models.Model):
    pacientes_rut = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='pacientes_rut')
    profesionales_rut = models.ForeignKey('Profesionales', models.DO_NOTHING, db_column='profesionales_RUT')  # Field name made lowercase.
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    estado_idestado = models.ForeignKey('Estado', models.DO_NOTHING, db_column='estado_idestado')
    status = models.IntegerField(blank=True, null=True)
    objects = AgendaManager()
    



class Estado(models.Model):
    idestado = models.AutoField(primary_key=True)
    desc_estado = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)


class Ficha(models.Model):
    nficha = models.AutoField(primary_key=True)
    profesionales_rut = models.ForeignKey('Profesionales', models.DO_NOTHING, db_column='profesionales_RUT')  # Field name made lowercase.
    pacientes_rut = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='pacientes_rut')
    motivoingreso = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    def registros(self):
        return Registro.objects.filter(nficha=self.nficha)
    


class Pacientes(models.Model):
    rut = models.CharField(primary_key=True, max_length=10)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    apellidos = models.CharField(max_length=255, blank=True, null=True)
    fechanacimiento = models.DateField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    objects = PacientesManager()
    def profesionales(self):
        return Ficha.objects.filter(pacientes_rut=self.rut, status=1)

class Profesionales(models.Model):
    rut = models.CharField(db_column='RUT', primary_key=True, max_length=10)  # Field name made lowercase.
    nombres = models.CharField(max_length=255, blank=True, null=True)
    apellidos = models.CharField(max_length=255, blank=True, null=True)
    numregistro = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    profesiones_idprofesiones = models.ForeignKey('Profesiones', models.DO_NOTHING, db_column='profesiones_idprofesiones')
    contrasena = models.CharField(max_length=255, blank=True, null=True)
    fechanacimiento = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    objects = ProfesionalesManager()
    


class Profesiones(models.Model):
    idprofesiones = models.AutoField(primary_key=True)
    desc_profesion = models.CharField(max_length=45, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    


class Registro(models.Model):
    idregistro = models.AutoField(primary_key=True)
    registro = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    status = models.IntegerField()
    nficha = models.ForeignKey(Ficha, models.DO_NOTHING, db_column='nficha')
