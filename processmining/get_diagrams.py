#!/usr/bin/env python3
'''
Implementaciones DFA probaiblista
   https://pypi.org/project/probabilistic-automata/
   sudo apt-get install graphviz
   labeling: https://graphviz.readthedocs.io/en/stable/examples.html
'''

from .Grafo import Grafo
from .drawgraphs import *
import time


def get_transition_probs(objeto):
   get_graph(objeto.lista_nodos, objeto.lista_probabilidad_transicion, objeto.lista_nodos_finales)

   return 0

def get_dijktra_probs(objeto,logaritmico):
   if logaritmico:
      list_of_graph = objeto.get_disktra(objeto.lista_probabilidad_transicion_logaritmica,logaritmico)

   else:
      list_of_graph = objeto.get_disktra(objeto.lista_probabilidad_transicion,objeto.lista_nodos_finales,logaritmico)


   for grafo_k in list_of_graph.keys():
       get_dijktra_graph(list_of_graph.get(grafo_k),objeto.lista_nodos_finales,grafo_k,logaritmico,objeto.lista_probabilidad_transicion)


   return 0

def get_AFD_apriori():
   objeto = Grafo()
   objeto.get_transitions('actividades_def.txt')
   transiciones = objeto.lista_transiciones

   objeto.get_nodes(transiciones)
   objeto.get_probabilities(transiciones)
   objeto.get_finalstate_prob()
   objeto.get_transition_probabilities()
   objeto.get_logaritmic_probs()
   get_transition_probs(objeto)

def get_AFD_djisktra():
   objeto = Grafo()
   objeto.get_transitions('actividades_def.txt')
   objeto.get_nodes(objeto.lista_transiciones)
   objeto.get_probabilities(objeto.lista_transiciones)
   objeto.get_finalstate_prob()
   objeto.get_transition_probabilities()
   objeto.get_logaritmic_probs()
   get_dijktra_probs(objeto, True)

