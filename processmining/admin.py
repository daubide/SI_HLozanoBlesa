from django.contrib import admin
from .models import PACIENTE,PROCEDIMIENTOS,PROFESIONAL,ACTIVIDAD, RECURSO, AREAPROFESIONAL,ACTIVIDAD_PACIENTE
# Register your models here.


admin.site.register(PACIENTE)
admin.site.register(AREAPROFESIONAL)
admin.site.register(PROCEDIMIENTOS)
admin.site.register(PROFESIONAL)
admin.site.register(ACTIVIDAD)
admin.site.register(RECURSO)
admin.site.register(ACTIVIDAD_PACIENTE)