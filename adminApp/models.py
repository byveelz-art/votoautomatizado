# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Auditoria(models.Model):
    id_evento = models.AutoField(primary_key=True)
    fecha_hora_evento = models.DateTimeField()
    entidad_afectada = models.CharField(max_length=50)
    id_registro_afectado = models.IntegerField(blank=True, null=True)
    tipo_evento = models.CharField(max_length=6)
    usuario_sistema = models.CharField(max_length=50)
    terminal = models.ForeignKey('Terminal', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditoria'


class CandidatoOpcion(models.Model):
    candidato_id = models.AutoField(primary_key=True)
    eleccion = models.ForeignKey('Eleccion', models.DO_NOTHING)
    nombre_candidato = models.CharField(max_length=100)
    cargo = models.CharField(max_length=50, blank=True, null=True)
    partido = models.CharField(max_length=50, blank=True, null=True)
    lista = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'candidato_opcion'


class Eleccion(models.Model):
    eleccion_id = models.AutoField(primary_key=True)
    tipo_eleccion = models.CharField(max_length=13)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_eleccion = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'eleccion'


class SesionVotacion(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    id_votante = models.ForeignKey('Votante', models.DO_NOTHING, db_column='id_votante')
    terminal = models.ForeignKey('Terminal', models.DO_NOTHING)
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    estado_sesion = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sesion_votacion'


class Terminal(models.Model):
    terminal_id = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    estado_terminal = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'terminal'


class UsuarioSistema(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=13, blank=True, null=True)
    id_votante = models.ForeignKey('Votante', models.DO_NOTHING, db_column='id_votante', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario_sistema'


class Votante(models.Model):
    id_votante = models.AutoField(primary_key=True)
    rut = models.CharField(unique=True, max_length=12)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100, blank=True, null=True)
    cod_qr = models.CharField(max_length=256)
    activo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'votante'


class Voto(models.Model):
    id_voto = models.AutoField(primary_key=True)
    id_sesion = models.ForeignKey(SesionVotacion, models.DO_NOTHING, db_column='id_sesion')
    tipo_eleccion = models.CharField(max_length=13)
    fecha_hora_emision = models.DateTimeField()
    voto_encriptado = models.TextField()
    hash_verificacion = models.CharField(max_length=256)
    comprobante_emision = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'voto'
