import time
from graphviz import Digraph
from dijkstar import Graph, find_path
import math

class Grafo:
    lista_transiciones = []
    lista_nodos = []
    lista_probabilidades_apriori = dict()
    lista_probabilidad_estado_final = dict()
    lista_probabilidad_transicion = dict()
    lista_probabilidad_transicion_logaritmica = dict()
    lista_probabilidad_transicion_logaritmica_min = dict()
    lista_nodos_finales = dict()
    max_logP = 0

    def __init__(self):
        print('Creando Nueva clase')

    def get_transitions(self,path_fichero):
        diccionario_estados = dict()
        try:
            with open(path_fichero) as f:

                for linea in f:
                    estado_anterior = ""
                    for estado in linea.split(";"):
                        key = estado_anterior + ";" + estado
                        key = key.rstrip()
                        if key in diccionario_estados:
                            diccionario_estados[key] = diccionario_estados.get(key) + 1
                        else:
                            diccionario_estados[key] = 1

                        estado_anterior = estado
                    estado = estado.strip('\n')
                    if estado not in self.lista_nodos_finales.keys():
                        self.lista_nodos_finales[estado] = 1
                    else:
                        last_value = self.lista_nodos_finales[estado]
                        self.lista_nodos_finales[estado] = last_value+1

                self.lista_transiciones = diccionario_estados
                return diccionario_estados
        except Exception as e:
            print("Ha ocurrido un error: " + str(e))

    def get_nodes(self,dict_transitions):
        '''

        :param dict_transitions:        diccionario de la siguiente forma [Origen;Destino]->
                                        siendo n el numero de veces que aparece esa tupla de
                                        transiciones.
        :return: list_nodos:            Lista [01,O3,O4...] Con los diferentes lista única de nodos
        '''
        lista_nodos = []
        for key in dict_transitions.keys():
            origen_destino = key.split(";")
            origen = origen_destino[0]
            destino = origen_destino[1]
            if (origen != " ") and (origen not in lista_nodos):
                lista_nodos.append(origen)
            if (destino != " ") and (destino not in lista_nodos):
                lista_nodos.append(destino)
        self.lista_nodos = lista_nodos
        return lista_nodos

    def get_finalstate_prob(self):
        total_final_states = sum(self.lista_nodos_finales.values())
        for nodo_final in self.lista_nodos_finales.keys():
            self.lista_probabilidad_estado_final[nodo_final] = round(float(self.lista_nodos_finales[nodo_final] \
                                                               / total_final_states),2)

        return  self.lista_probabilidad_estado_final

    def get_transition_probabilities(self):
        '''

            :return: dict_prob Origen;Destino -> N
                    siendo n un numero [0,1] que indica la probaiblidad de la transición
        '''
        for key in self.lista_probabilidades_apriori.keys():
            # Se cogen todos los origenes guardados
            origen_destino = key.split(";")
            origen = origen_destino[0]
            destino = origen_destino[1]
            probabilidad_apriori = self.lista_probabilidades_apriori[key]


            if origen in self.lista_probabilidad_estado_final.keys():
                prob_estadofinal = self.lista_probabilidad_estado_final[origen]
                if prob_estadofinal != 0:
                    self.lista_probabilidad_transicion[key] = float(probabilidad_apriori * (1-prob_estadofinal))
                else:
                    self.lista_probabilidad_transicion[key] = float(probabilidad_apriori)
            else:
                self.lista_probabilidad_transicion[key] = float(probabilidad_apriori)

        return self.lista_probabilidad_transicion

    def get_probabilities(self,dict_transitions):
        '''

        :param      dict_transitions:   diccionario de la siguiente forma [Origen;Destino]->
                                        siendo n el numero de veces que aparece esa tupla de
                                        transiciones.
        :return:    dict_prob Origen;Destino -> N
                    siendo n un numero [0,1] que indica la probabilidad a priori

        '''
        dict_origenes = dict()  # Diccionario que recoge los origenes
        dict_prob = dict()  # Diccionaro de
        for key in dict_transitions.keys():
            # Se cogen todos los origenes guardados
            origen_destino = key.split(";")
            origen = origen_destino[0]

            if not origen in dict_origenes.keys():
                # No tenemos ese origen guardado
                # Recorremos la lista otra vez para ver que mas origenes encontramos duplicados
                for key2 in dict_transitions.keys():
                    origen_destino2 = key2.split(";")
                    origen2 = origen_destino2[0]
                    if origen2 == origen:
                        if origen in dict_origenes.keys():
                            dict_origenes[origen] += dict_transitions.get(key2)
                        else:
                            dict_origenes[origen] = dict_transitions.get(key2)

        for key_trans in dict_transitions:
            origen_destino = key_trans.split(";")
            origen_trans = origen_destino[0]        # Origen
            dict_prob[key_trans]= float(dict_transitions.get(key_trans) / dict_origenes[origen_trans])



        self.lista_probabilidades_apriori = dict_prob
        return dict_prob

    def get_logaritmic_probs(self):
        for clave_transicion in self.lista_probabilidad_transicion.keys():
            origen_destino = clave_transicion.split(";")
            valor_transicion = float(self.lista_probabilidad_transicion.get(clave_transicion))
            origen = origen_destino[0]
            destino = origen_destino[1]
            new_value = round(float(-math.log(valor_transicion)),2)
            if new_value == -0.0:
                self.lista_probabilidad_transicion_logaritmica[clave_transicion] = 0
            else:
                self.lista_probabilidad_transicion_logaritmica[clave_transicion] = new_value
            nueva_clave_origen = origen+';'+origen+'_l'
            nueva_clave_destino = destino+';'+destino+'_l'

            if (origen in self.lista_nodos_finales.keys()) and \
                    (nueva_clave_origen not in self.lista_probabilidad_transicion_logaritmica) :

                prob_final_stateo = self.lista_probabilidad_estado_final.get(origen)
                self.lista_probabilidad_transicion_logaritmica[nueva_clave_origen] = round(float(-math.log(prob_final_stateo)),2)

            if (destino in self.lista_nodos_finales.keys()) and \
                    (nueva_clave_destino not in self.lista_probabilidad_transicion_logaritmica):
                prob_final_stated = self.lista_probabilidad_estado_final.get(destino)
                self.lista_probabilidad_transicion_logaritmica[nueva_clave_destino] = round(float(-math.log(prob_final_stated)),2)

        self.max_logP = max(self.lista_probabilidad_transicion_logaritmica.values())
        return self.lista_probabilidad_transicion_logaritmica

    def get_minimum_logaritmic_probs(self):
        for clave_transicion in self.lista_probabilidad_transicion.keys():
            origen_destino = clave_transicion.split(";")
            valor_transicion = float(self.lista_probabilidad_transicion.get(clave_transicion))
            origen = origen_destino[0]
            destino = origen_destino[1]
            new_value = round(math.fabs( round(float(-math.log(valor_transicion)), 2) - self.max_logP),2)
            if new_value == -0.0:
                self.lista_probabilidad_transicion_logaritmica_min[clave_transicion] = 0
            else:
                self.lista_probabilidad_transicion_logaritmica_min[clave_transicion] = new_value
            nueva_clave_origen = origen + ';' + origen + '_l'
            nueva_clave_destino = destino + ';' + destino + '_l'

            if (origen in self.lista_nodos_finales.keys()) and \
                    (nueva_clave_origen not in self.lista_probabilidad_transicion_logaritmica_min):
                prob_final_stateo = self.lista_probabilidad_estado_final.get(origen)
                self.lista_probabilidad_transicion_logaritmica_min[nueva_clave_origen] = round(math.fabs(round(
                    float(-math.log(prob_final_stateo)), 2) - self.max_logP),2)

            if (destino in self.lista_nodos_finales.keys()) and \
                    (nueva_clave_destino not in self.lista_probabilidad_transicion_logaritmica_min):
                prob_final_stated = self.lista_probabilidad_estado_final.get(destino)
                self.lista_probabilidad_transicion_logaritmica_min[nueva_clave_destino] = round(math.fabs(round(
                    float(-math.log(prob_final_stated)), 2)-self.max_logP),2)

        return self.lista_probabilidad_transicion_logaritmica_min

    def get_disktra(self,dict_probabilities,logaritmico):
        # Return a Graph to apply djistra algorithm
        grafo = Graph()
        dict_of_graphs = dict()

        for clave_transicion in dict_probabilities.keys():
            origen_destino = clave_transicion.split(";")
            origen = origen_destino[0]
            destino = origen_destino[1]
            valor_transicion = str(dict_probabilities.get(clave_transicion))
            grafo.add_edge(origen, destino, int(float(valor_transicion)*100))

        for final_node in self.lista_nodos_finales:
           if logaritmico:
               dict_of_graphs[final_node] = find_path(grafo, "", final_node+'_l')
           else:
               dict_of_graphs[final_node] = find_path(grafo, "", final_node)

        return dict_of_graphs







