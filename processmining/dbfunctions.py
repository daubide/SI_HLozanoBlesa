from django.db import models
from django.utils.timezone import now as timezone_now
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import PACIENTE,PROCEDIMIENTOS,PROFESIONAL,ACTIVIDAD, RECURSO, AREAPROFESIONAL

def get_profesional_name(iden):
    return PROFESIONAL.objects.get(identificador_medico = iden).nombre