from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'iniciarsesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path(r'listaProcedimientos/', views.listaDeProcedimientos, name='listaDeProcedimientos'),
    path(r'listaDeActividades/', views.listaDeActividades, name='ListaDeActividades'),
    path(r'listaDeRecursos/', views.listaDeRecursos, name='ListaRecursos'),
    path(r'listaDePacientes/', views.listaDePacientes, name='ListaDePacientes'),
    path(r'listaLogs/', views.listaDeLogs, name='ListaLogs'),
    path(r'desconexion/', views.desconexion, name='desconexion'),
    path(r'recuperarContrasena/', views.recuperarContrasena, name='contrasena'),
    path(r'recuperarContrasena/inicio', views.recuperarContrasena, name='contrasena'),
    path(r'listaminData/', views.listaDeMineriaDatos, name='returninicio'),
]
