
from graphviz import Digraph
from graphviz import Graph as gp
from dijkstar import Graph, find_path

" Use graphviz to draw different graphs"
def get_graph(list_nodos, dict_transiciones,lista_nodos_finales):

    f = Digraph('finite_state_machine', filename='medical_graph',format='pdf')
    f.attr(rankdir='LR', size='20.5')

    for nodo in list_nodos:


        if nodo in lista_nodos_finales.keys():
            f.attr('node', shape='doublecircle')
        else:
            f.attr('node', shape='circle')
        f.node(nodo)

    for clave_transicion in dict_transiciones.keys():
        origen_destino = clave_transicion.split(";")
        origen = origen_destino[0]
        destino = origen_destino[1]
        valor_transicion = str( "{:.0%}".format(dict_transiciones.get(clave_transicion)))
        f.edge(origen, destino, label=valor_transicion)

    #f.node('',label= main_label)
    # f.view() # Vista residual en el archivo
    f.render('test-output/grafo_medico', view=True)

def get_dijktra_graph(grafo,lista_nodos_finales,title,logaritmico,dict_transiciones,type):
    f = Digraph('finite_state_machine', filename='medical_graph',format='pdf')
    f.attr(rankdir='LR', size='20.5')
    print(grafo)

    for nodo in grafo.nodes:
        if not "_l" in nodo:

            if nodo in lista_nodos_finales.keys():
                f.attr('node', shape='doublecircle')
            else:
                f.attr('node', shape='circle')
            f.node(nodo)

    counter = 0
    for edges_cost in grafo.edges:
        nodo_origen = grafo.nodes[counter]
        nodo_destino = grafo.nodes[counter+1]
        origen_destino= nodo_origen+';'+nodo_destino
        if not "_l" in nodo_destino:
            if logaritmico:
                f.edge(grafo.nodes[counter], grafo.nodes[counter+1],
                       label=str("{0:.0%}".format(dict_transiciones.get(origen_destino))))
            else:
              f.edge(grafo.nodes[counter], grafo.nodes[counter+1], label=str("{0:.0%}".format(float(edges_cost/100))))
        counter=counter+1
    if type == 1:
        f.render('test-output/dijktraGraph_max'+title, view=True)
    if type == 2:
        f.render('test-output/dijktraGraph_min'+title, view=True)
