from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from .models import PACIENTE,PROCEDIMIENTOS,PROFESIONAL,ACTIVIDAD, RECURSO, AREAPROFESIONAL,ACTIVIDAD_PACIENTE
from django.http import HttpResponse
from django.db.models import *
from .dbfunctions import *
from xlrd import *
from datetime import datetime

def poblate_procedimientos():
    p = PROCEDIMIENTOS.objects.create(nombre_procedimiento= "Artroplastia cadera")
    p.save()
    print("Poblado procedimientos adecuadamente")

def poblate_area_profesional(Area):
    p = AREAPROFESIONAL.objects.create(nombre_area= Area)
    p.save()
    print("Poblado area_profesional adecuadamente")



def poblate_profesional():
    wb = open_workbook('./processmining/pacientes_def.xlsx')
    sheet = wb.sheet_by_index(2)
    number_of_rows = sheet.nrows

    for row in range (1,number_of_rows):
        idmedico_t = int(sheet.cell(row,0).value)
        Nombre_t = sheet.cell(row, 1).value
        Apellidos_t = sheet.cell(row, 2).value
        Categoria_profesional = sheet.cell(row, 3).value
        Edad_t = int(sheet.cell(row, 4).value)
        Area_t = sheet.cell(row, 5).value
        try:
            try:
                area_destino = AREAPROFESIONAL.objects.get(nombre_area=Area_t)
            except:
                poblate_area_profesional(Area_t)
                area_destino = AREAPROFESIONAL.objects.get(nombre_area= Area_t)

            try:
                PROFESIONAL.objects.get(identificador_medico= idmedico_t)
            except:
                profesional_t = PROFESIONAL(
                    identificador_medico = idmedico_t,
                    nombre= str(Nombre_t),
                    tipo_profesional = str(Categoria_profesional),
                    apellidos= str(Apellidos_t),
                    edad=Edad_t,
                    area_prof = area_destino,

                )
                profesional_t.save()
                print("Creado profesional: " + str(profesional_t))

        except Exception as e :
             print("Query incorrecta, no se ha podido crear el modelo: "+str(e))
             return 0
    print("Poblado profesionales adecuadamente")


def poblate_pacientes():
    wb = open_workbook('./processmining/pacientes_def.xlsx')
    sheet = wb.sheet_by_index(4)
    number_of_rows = sheet.nrows

    for row in range(1, number_of_rows):
        idmedico_t = int(sheet.cell(row, 0).value)
        sexo = sheet.cell(row, 1).value
        origen_t = sheet.cell(row, 2).value
        Edad_t = int(sheet.cell(row, 3).value)
        Dia_ingreso = int(sheet.cell(row, 4).value)
        Dia_ingreso_t = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + Dia_ingreso - 2)
        motivo_intervencion_t = sheet.cell(row, 5).value
        Cirujano_principal = sheet.cell(row, 6).value

        if PROFESIONAL.objects.filter(apellidos=Cirujano_principal).exists():
            cirujano_destino = PROFESIONAL.objects.get(apellidos=Cirujano_principal)
        else:
            print("No existe el cirujano:"+ Cirujano_principal)
            break

        try:
            procedimiento = PROCEDIMIENTOS.objects.get(nombre_procedimiento="Artroplastia cadera")
        except:
            poblate_procedimientos()
            print("Procedimiento creado adecuadamente: " + "Artroplastia cadera")

        procedimiento = PROCEDIMIENTOS.objects.get(nombre_procedimiento="Artroplastia cadera")
        paciente_t = PACIENTE(
            identificador_medico=idmedico_t,
            sexo_paciente=sexo,
            origen_paciente=origen_t,
            fecha_inclusion=Dia_ingreso_t.strftime('%Y-%m-%d'),
            edad=Edad_t,
            diagnostico= motivo_intervencion_t,
            procedimiento_paciente = procedimiento,
            profesional_paciente=cirujano_destino,

        )
        paciente_t.save()
        print("Creado paciente: " + str(paciente_t))
def poblate_recursos():

    wb = open_workbook('./processmining/pacientes_def.xlsx')
    sheet = wb.sheet_by_index(5)
    number_of_rows = sheet.nrows

    for row in range(1, number_of_rows):
        try:
            nombre_recurso_t = sheet.cell(row, 0).value
            tipo_recurso_t = sheet.cell(row, 1).value
            recurso_t = RECURSO(
                nombre_recurso =nombre_recurso_t,
                tipo=tipo_recurso_t
            )
            recurso_t.save()
            print(nombre_recurso_t+ " creado adecuadamente")
        except Exception as e:
            print("Error al crear recurso: "+str(e))
            return 0
    return 1

def poblate_actividades():
    wb = open_workbook('./processmining/pacientes_def.xlsx')
    sheet = wb.sheet_by_index(3)
    number_of_rows = sheet.nrows

    for row in range(1, number_of_rows):

        nombre_actividad_ = sheet.cell(row, 0).value
        recurso_1 = sheet.cell(row, 1).value
        recurso_2 = sheet.cell(row, 2).value

        actividad_t = ACTIVIDAD(
            nombre_actividad =nombre_actividad_
        )
        try:
            actividad_t.save()

        except Exception as e:
            print("No se ha podido crear la actividad: "+nombre_actividad_+ "\n" +str(e))

        try:
            recurso_2o= RECURSO.objects.get(nombre_recurso =recurso_2)
            actividad_t.recurso_asociado.add(recurso_2o)
        except:
            print("No existe segundo recurso en " + nombre_actividad_ )
        if not  "Reposo" in nombre_actividad_ :
            print("Voy a buscar recurso para:" +nombre_actividad_)
            recurso_1o = RECURSO.objects.get(nombre_recurso=recurso_1)
            actividad_t.recurso_asociado.add(recurso_1o)


        print(str(actividad_t) + " creado adecuadamente")

def poblate_actividad_paciente():
    wb = open_workbook('./processmining/pacientes_def.xlsx')
    sheet = wb.sheet_by_index(1)
    number_of_rows = sheet.nrows

    for row in range(2, number_of_rows):
            first_value = sheet.cell(row, 1).value
            if not first_value == '':
                id_paciente_t = int(first_value)
                dia_actividad = int(sheet.cell(row, 2).value)
                actividad_realizada = sheet.cell(row,4).value
                paciente_t = PACIENTE.objects.get(identificador_medico = id_paciente_t)
                try:
                    if "Reposo" in actividad_realizada:
                        actividad_realizada = actividad_realizada+str(dia_actividad)

                    actividad_t = ACTIVIDAD.objects.get(nombre_actividad = actividad_realizada)

                    try:
                        actividad_paciente = ACTIVIDAD_PACIENTE(
                            id_paciente = paciente_t,
                            id_actividad = actividad_t,
                            duracion = dia_actividad
                        )
                        actividad_paciente.save()
                        print("Actividad-paciente_guardado: " + str(actividad_t.nombre_actividad))

                    except Exception as e:
                        print("No se ha podido guardar el paciente en la bd  " + str(e) +" " +actividad_realizada)
                        return 0
                except:
                    print("No se ha encontrado la actividad: "+ actividad_realizada)
                    return 0
    return 1