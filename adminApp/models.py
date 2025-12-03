from django.db import models


class Terminal(models.Model):
    terminal_id = models.AutoField(primary_key=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    estado_terminal = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        db_table = 'terminal'
    
    def __str__(self):
        return f"Terminal {self.terminal_id} - {self.ubicacion} ({self.estado_terminal})"


class Eleccion(models.Model):
    eleccion_id = models.AutoField(primary_key=True)
    tipo_eleccion = models.CharField(max_length=13)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado_eleccion = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        db_table = 'eleccion'
    
    def __str__(self):
        return f"{self.tipo_eleccion} ({self.fecha_inicio} - {self.fecha_fin})"


class Votante(models.Model):
    id_votante = models.AutoField(primary_key=True, auto_created=False)
    rut = models.CharField(unique=True, max_length=12)
    nombre = models.CharField(max_length=50)
    apellido_paterno = models.CharField(max_length=50)
    apellido_materno = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    direccion = models.CharField(max_length=100, blank=True, null=True)
    cod_qr = models.CharField(max_length=256)
    activo = models.IntegerField(blank=True, null=True, default=1)

    class Meta:
        db_table = 'votante'
    
    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno} (RUT: {self.rut})"


class Auditoria(models.Model):
    id_evento = models.AutoField(primary_key=True)
    fecha_hora_evento = models.DateTimeField()
    entidad_afectada = models.CharField(max_length=50)
    id_registro_afectado = models.IntegerField(blank=True, null=True)
    tipo_evento = models.CharField(max_length=6)
    usuario_sistema = models.CharField(max_length=50)
    terminal = models.ForeignKey(
        Terminal, 
        on_delete=models.SET_NULL,
        blank=True, 
        null=True
    )

    class Meta:
        db_table = 'auditoria'


class SesionVotacion(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    id_votante = models.ForeignKey(
        Votante,
        on_delete=models.CASCADE,
        db_column='id_votante'
    )
    terminal = models.ForeignKey(
        Terminal, 
        on_delete=models.CASCADE
    )
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    estado_sesion = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'sesion_votacion'


class CandidatoOpcion(models.Model):
    class eleccionTipo(models.TextChoices):
        PRESIDENCIAL = 'Presidencial'
        PARLAMENTARIA = 'Parlamentaria'
        MUNICIPAL = 'Municipal'
    class cargoTipo(models.TextChoices):
        SENADOR = 'Senador'
        DIPUTADO = 'Diputado'
        ALCALDE = 'Alcalde'
        CONCEJAL = 'Concejal'
    candidato_id = models.AutoField(primary_key=True)
    eleccion = models.CharField(choices=eleccionTipo.choices)
    nombre_candidato = models.CharField(max_length=100)
    cargo = models.CharField(choices=cargoTipo.choices, default="Sin cargo", null=True)
    partido = models.CharField(max_length=50, blank=True, null=True)
    lista = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'candidato_opcion'

    def __str__(self):
        return f"{self.nombre_candidato} - {self.cargo} ({self.partido})"

class UsuarioSistema(models.Model):
    class UsuarioRol(models.TextChoices):
        ADMIN = 'Admin'
        VOTANTE = 'Votante'
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(choices=UsuarioRol.choices, blank=True, null=True)
    id_votante = models.ForeignKey(
        Votante,
        on_delete=models.SET_NULL,
        db_column='id_votante',
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'usuario_sistema'

    def __str__(self):
        return f"{self.username} ({self.rol})"

class Voto(models.Model):
    id_voto = models.AutoField(primary_key=True)
    id_sesion = models.ForeignKey(
        SesionVotacion,
        on_delete=models.CASCADE,
        db_column='id_sesion'
    )
    tipo_eleccion = models.CharField(max_length=13)
    fecha_hora_emision = models.DateTimeField()
    voto_encriptado = models.TextField()
    hash_verificacion = models.CharField(max_length=256)
    comprobante_emision = models.CharField(unique=True, max_length=100)
    id_candidato = models.ForeignKey(CandidatoOpcion, on_delete=models.CASCADE)
    pdf_file = models.FileField(default=None, null=True, blank=True)

    class Meta:
        db_table = 'voto'
    
    def __str__(self):
        return f"Voto {self.id_voto} - Sesión {self.id_sesion.id_sesion} - Elección {self.tipo_eleccion}"

