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
from .poblatedb import *
from .for_medical import *
from .test_diagramas import get_AFD_apriori
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    #poblar_db()
    return render(request, 'index.html')

@csrf_protect
def iniciar_sesion(request):

    user_f = request.POST['userf']
    password_f = request.POST['passf']

    user = authenticate(username=user_f, password=password_f)

    if user is not None:
        nombre_facultativo = get_profesional_name(user_f)
        request.session['name'] = nombre_facultativo
        request.session['idprof'] = user_f
        pacientes = PACIENTE.objects.filter(profesional_paciente = user_f)
        return render(request, 'ListaDePacientes.html',{'pacientes': pacientes })
    else:
        mensaje = 'Correo y/o contraseña incorrectos'
        error_m = {'errormessage': mensaje}
        return render(request,"index.html",error_m)



def desconexion(request):
    for key in list(request.session.keys()):
        print(key)
        if not key.startswith("_"):
            del request.session[key]
    return redirect('/processmining/')


def listaDeMineriaDatos(request):
    return render(request, 'Lista_minData.html')

def listaDeActividades(request):
    last_index_log = request.GET.get('page', 1)
    actividades = ACTIVIDAD.objects.all()
    paginas = Paginator(actividades, 6)
    paginas_ = paginas.page(1)
    try:
        paginas_ = paginas.page(last_index_log)
    except PageNotAnInteger:
        paginas_ = paginas.page(1)
    except EmptyPage:
        paginas_ = paginas.page(paginas.num_pages)
    return render(request, 'ListaDeActividades.html',{'actividades': paginas_})

def listaDePacientes(request):
    pacientes = PACIENTE.objects.filter(profesional_paciente=request.session['idprof'])
    return render(request, 'ListaDePacientes.html', {'pacientes': pacientes})

def listaDeLogs(request):
    listafinal = []

    last_index_log = request.GET.get('page', 1)

    operaciones = ACTIVIDAD_PACIENTE.objects.filter(id_paciente__profesional_paciente=request.session['idprof']).order_by('id_paciente','dia_inicio')
    paginas = Paginator(operaciones,10)
    paginas_ = paginas.page(1)
    try:
        paginas_ = paginas.page(last_index_log)
    except PageNotAnInteger:
        paginas_ = paginas.page(1)
    except EmptyPage:
        paginas_ = paginas.page(paginas.num_pages)
    '''
    for operacion in operaciones:
        if operacion.identificador_paciente.profesional_paciente == request.session['idprof']:
            listafinal.append(operacion)
    '''
    return render(request, 'ListaLogs.html',{'operaciones':paginas_ })

def listaDeProcedimientos(request):
    procedimientos = PROCEDIMIENTOS.objects.all()
    return render(request, 'ListaProcedimientos.html',{'procedimientos': procedimientos})

def listaDeRecursos(request):
    recursos = RECURSO.objects.all()
    return render(request, 'ListaRecursos.html',{'recursos': recursos})
def recuperarContrasena(request):
    return render(request, 'Recuperar_contrasena.html')

def activities_to_txt():
    actividad_pacientes = ACTIVIDAD_PACIENTE.objects.all().order_by('id_paciente','duracion')
    last_user = 0
    f = open("processmining/actividades_def.txt", "w+")
    to_write=""
    first = True
    for actividad_paciente in actividad_pacientes:
        usuario_actual = actividad_paciente.id_paciente

        if first:
            first = False
            to_write = to_write +actividad_paciente.id_actividad.nombre_actividad
            last_user = usuario_actual
        elif usuario_actual == last_user:
           to_write = to_write + ';'+ actividad_paciente.id_actividad.nombre_actividad
           print("We have added: " + to_write)

        else:
            to_write= to_write+"\n"+actividad_paciente.id_actividad.nombre_actividad
            last_user = usuario_actual

    f.write(to_write)
    f.close()
    return 0
def poblar_db():
    poblate_procedimientos()
    poblate_profesional()
    poblate_pacientes()
    poblate_recursos()
    poblate_actividades()
    poblate_actividad_paciente()

def get_apriori_diagram():
    get_AFD_apriori()

def get_diijktradiagram():
    get_AFD_djisktra()

def get_RDP():
    lista_recursos = []
    lista_nodos = []
    lista_transiciones = []
    list_place_resource = {}
    QS_recursos  = RECURSO.objects.all()
    QS_actvidades = ACTIVIDAD.objects.all()
    for recurso in QS_recursos:
        lista_recursos.append(recurso.nombre_recurso.replace(" ",""))
    for actividad  in QS_actvidades:
        if actividad.recurso_asociado.all():
            list_place_resource[actividad.nombre_actividad.replace(" ","")] = []
            for recurso in actividad.recurso_asociado.all():

                list_place_resource[actividad.nombre_actividad.replace(" ","")].append(recurso.nombre_recurso.replace(" ",""))
    with open("processmining/listanodos.txt") as f:
        for linea in f:
            for nodo in linea.split(";"):
                if nodo not in lista_nodos:
                    lista_nodos.append(nodo.rstrip().replace(" ",""))
    with open("processmining/listatransiciones.txt") as f:
        for linea in f:
            for transicion in linea.split(","):
                if transicion not in lista_nodos:
                    lista_transiciones.append(transicion.rstrip().replace(" ",""))
    create_CPN('cpn_protesiscadera', lista_nodos, lista_recursos, lista_transiciones, list_place_resource)
    return True



