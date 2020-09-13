from django.db import models
from django.utils.timezone import now as timezone_now
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.




class PROCEDIMIENTOS(models.Model):
    nombre_procedimiento = models.CharField(
        null=False,
        max_length=100
    )


class AREAPROFESIONAL(models.Model):
    nombre_area = models.CharField(
        max_length=100,
        primary_key=True
    )

    def __str__(self):
        return self.nombre_area


class PROFESIONAL(models.Model):

    identificador_medico = models.IntegerField(
        null=False,
        default=-1,
        primary_key=True
    )

    nombre = models.CharField(
        null=False,
        default='',
        max_length=150
    )

    apellidos = models.CharField(
        null=False,
        default='',
        max_length=150
    )
    tipo_profesional = models.CharField(
        null=False,
        default='',
        max_length=150,
    )
    edad = models.IntegerField(
        null=False
    )

    area_prof = models.ForeignKey(
        default= '',
        to=AREAPROFESIONAL,
        null=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.apellidos



class RECURSO(models.Model):
    nombre_recurso = models.CharField(
        null=False,
        max_length=50
    )
    tipo = models.CharField(
        null=False,
        max_length=50
    )

    def __str__(self):
        return self.nombre_recurso



class PACIENTE(models.Model):
    identificador_medico = models.IntegerField(
        null=False,
        default=-1,
        primary_key=True
    )
    sexo_paciente = models.CharField(
        default = '',
        null=False,
        max_length=150,
    )

    origen_paciente = models.CharField(
        default = '',
        null=False,
        max_length=150,
    )

    edad = models.IntegerField(
        null=False
    )
    fecha_inclusion = models.DateField(
        default=timezone_now
    )
    diagnostico = models.CharField(
        null=False,
        max_length=150
    )
    procedimiento_paciente = models.ForeignKey(
        default = '',
        to=PROCEDIMIENTOS,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='tipo de procedimiento asociado a un paciente'
    )

    profesional_paciente = models.ForeignKey(
        default = '',
        null = False,
        to=PROFESIONAL,
        on_delete=models.CASCADE,
        verbose_name='Profesional asociado a un paciente'
    )



class ACTIVIDAD(models.Model):
    nombre_actividad = models.CharField(
        null=False,
        max_length=50
    )

    recurso_asociado = models.ManyToManyField(
        to=RECURSO,
        verbose_name='tipo de recuerso profesional asociado a una actividad'
    )

    def __str__(self):
        return self.nombre_actividad




class ACTIVIDAD_PACIENTE(models.Model):
    id_paciente = models.ForeignKey(
        default='',
        null=False,
        to=PACIENTE,
        on_delete=models.CASCADE,
        verbose_name='Identificador del paciente al que se le aplica'
    )
    id_actividad = models.ForeignKey(
        default='',
        null=False,
        to=ACTIVIDAD,
        on_delete=models.CASCADE,
        verbose_name='Identificador de la actividad asociada'
    )

    dia_inicio = models.PositiveIntegerField(
        null=False,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    duracion = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return self.id_actividad.nombre_actividad + "aplicada al paciente: " + str(self.id_paciente)

