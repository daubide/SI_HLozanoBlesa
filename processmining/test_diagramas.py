'''
Implementaciones DFA probaiblista
   https://pypi.org/project/probabilistic-automata/
   sudo apt-get install graphviz
   labeling: https://graphviz.readthedocs.io/en/stable/examples.html
'''

from .Grafo import Grafo
from .drawgraphs import *


def get_transition_probs(objeto):
   get_graph(objeto.lista_nodos, objeto.lista_probabilidad_transicion, objeto.lista_nodos_finales)

   return 0

def get_dijktra_probs(objeto,logaritmico,type):
   if logaritmico:
      if type==1:
         list_of_graph = objeto.get_disktra(objeto.lista_probabilidad_transicion_logaritmica,logaritmico)
      else:
         list_of_graph = objeto.get_disktra(objeto.lista_probabilidad_transicion_logaritmica_min, logaritmico)
   else:
      list_of_graph = objeto.get_disktra(objeto.lista_probabilidad_transicion,objeto.lista_nodos_finales,logaritmico)


   for grafo_k in list_of_graph.keys():
         get_dijktra_graph(list_of_graph.get(grafo_k), objeto.lista_nodos_finales, grafo_k, logaritmico,objeto.lista_probabilidad_transicion, type)
   return 0


def get_AFD_apriori():
   objeto = Grafo()
   objeto.get_transitions('actividades_def.txt')
   objeto.get_nodes(objeto.lista_transiciones)
   objeto.get_probabilities(objeto.lista_transiciones)
   objeto.get_finalstate_prob()
   objeto.get_transition_probabilities()
   objeto.get_logaritmic_probs()
   get_transition_probs(objeto)
   return objeto

def get_AFD_djisktra_max():
   objeto = Grafo()
   objeto.get_transitions('actividades_def.txt')
   objeto.get_nodes(objeto.lista_transiciones)
   objeto.get_probabilities(objeto.lista_transiciones)
   objeto.get_finalstate_prob()
   objeto.get_transition_probabilities()
   objeto.get_logaritmic_probs()
   get_dijktra_probs(objeto, True,1)

def get_AFD_djisktra_min():
   objeto = Grafo()
   objeto.get_transitions('actividades_def.txt')
   objeto.get_nodes(objeto.lista_transiciones)
   objeto.get_probabilities(objeto.lista_transiciones)
   objeto.get_finalstate_prob()
   objeto.get_transition_probabilities()
   objeto.get_logaritmic_probs()
   objeto.get_minimum_logaritmic_probs()
   get_dijktra_probs(objeto, True,2)


