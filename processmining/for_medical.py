#!/usr/bin/env python3
# TFG: David Ubide Alaiz
import numpy as np
from sympy import *
from copy import deepcopy
import random

class CPN():

    def __init__(self,name=''):
        self.cpnName=name
        self.listPlaces={}
        self.list_places=[]
        self.listTrans=[]
        self.listArcs=[]
        self.listColors=[]
        self.composed_color = []

    def addPlace(self,place):
        self.listPlaces[place.placeName]=place

    def addTransition(self,trans):
        self.listTrans.append(trans)

    def addArc(self,arc):
        self.listArcs.append(arc)

    def addColor(self,color):
        self.listColors.append(color)

    def __str__(self):
        return("""CPN: {}\nPlaces: {}\nTransitions: {}\nColors: {}""".format(self.cpnName,self.listPlaces.keys(),self.listTrans,self.listColors))

    def generateXML(self,Id):
        """generate a xml file for cpn tool"""
        #Init of the string containing xml code
        xml="""<?xml version="1.0" encoding="iso-8859-1"?>\n"""
        xml+="""<!DOCTYPE workspaceElements PUBLIC "-//CPN//DTD CPNXML 1.0//EN" "http://cpntoold.org/DTD/6/cpn.dtd">\n"""
        xml+="""<workspaceElements>\n"""
        xml+="""<generator tool="CPN Tools" version="4.0.1" format="6"/>\n"""
        xml+="""<cpnet>\n"""

        ###Declarations
        xml+="""<globbox>\n"""

        #Priorities
        xml+="""<block>\n"""
        xml+="""<id>Standard priorities</id>\n"""
        xml+="""<ml>val P_HIGH = 100;\n<layout>val P_HIGH = 100;</layout>\n</ml>\n"""
        xml+="""<ml>val P_NORMAL = 1000;\n<layout>val P_NORMAL = 1000;</layout>\n</ml>\n"""
        xml+="""<ml>val P_LOW = 10000;\n<layout>val P_LOW = 10000;</layout>\n</ml>\n"""
        xml+="""</block>\n"""

        #Colors
        xml+="""<block>\n"""
        xml+="""<id>Declarations</id>\n"""
        vars=""
        for color in self.listColors:
            xml += """<color>\n"""
            xml += """<id>{}</id>\n""".format(color.colName)
            xml += """<string/>\n""".format(color.colName)
            xml += """<layout>colset {} = string;</layout>""".format(color.colName)
            xml += """</color>\n"""

            #Var associated with colors
            vars+="""<var>\n<type>\n<id>{}</id>\n</type>\n""".format(color.colName)
            vars+="""<id>{}</id>\n""".format(color.colVar)
            vars+="""<layout>var {} : {};</layout>\n""".format(color.colVar,color.colName)
            vars+="""</var>\n"""
        for composed_c in self.composed_color:
            xml += """<color>\n"""
            xml += """<id>{}</id>\n""".format(composed_c.colName)
            xml += """<product>\n"""
            for new_c in composed_c.listaColores:
                xml += """<id>{}</id>\n""".format(new_c.colName)
            xml += """</product>\n"""
            xml += """<layout>colset {} = product """.format(composed_c.colName)
            primero = True
            for new_c2 in composed_c.listaColores:
                if primero:
                    xml+=""" {}""".format(new_c2.colName)
                    primero = False
                else:
                    xml += """ * {}""".format(new_c2.colName)

            xml += """</layout> \n</color>\n"""

        xml+=vars
        xml+="""</block>\n"""
        xml+="""</globbox>\n"""
        ###

        ###Main Page
        idPage=Id
        Id+=1
        xml+="""<page id="ID{}">\n<pageattr name="Net"/>\n""".format(idPage)

        #Places
        places=""
        for pl in self.listPlaces:
            currPl=self.listPlaces[pl]
            places+="""<place id="ID{}">\n""".format(currPl.id)
            places+="""<text>{}</text>\n""".format(currPl.placeName)
            places+="""<ellipse w="60.0" h="40.0"/>\n""" #Just for visual conveniance
            places+="""<type>\n"""
            places+="""<posattr x="50.0" y="-23.0"/>\n"""
            if currPl.compose_color:
                places += """<text tool="CPN Tools" version="4.0.1">{}</text>\n""".format(currPl.compose_color.colName)
            else:
                places+="""<text tool="CPN Tools" version="4.0.1">{}</text>\n""".format(currPl.placeColor.colName)
            places+="""</type>\n"""
            places+="""<initmark>\n"""
            places+="""<posattr x="40.0" y="23.0"/>\n"""
            if currPl.marks == 0:
                places+="""<text tool="CPN Tools" version="4.0.1"/>\n"""
            else:
                places+="""<text tool="CPN Tools" version="4.0.1">{}`&quot;{}&quot;</text>\n""".format(currPl.marks,currPl.initMarking)
            places+="""</initmark>\n</place>\n"""

        xml+=places

        #Transitions

        transi=""
        for tr in self.listTrans:
            transi+="""<trans id="ID{}" explicit="false">\n""".format(tr.id)
            transi+="""<text>{}</text>\n""".format(tr.transName)
            transi+="""<box w="60.0" h="40.0"/>\n""" #For visual conveniance
            transi+="""</trans>\n"""

        xml+=transi

        #Arcs

        arcs=""
        for a in self.listArcs:
            arcs+="""<arc orientation="{}" order="1">\n""".format(a.type)
            arcs+="""<transend idref="ID{}"/>\n""".format(a.trans.id)
            arcs+="""<placeend idref="ID{}"/>\n""".format(a.place.id)
            arcs+="""<annot>\n"""
            place_arc = a.place
            if place_arc.compose_color:
                arcs += """<text tool="CPN Tools" version="4.0.1">("""
                primero = True
                for color_a in place_arc.compose_color.listaColores:
                    if primero:
                        arcs+="""{}""".format(color_a.colName)
                        primero = False
                    else:
                        arcs += """,{}""".format(color_a.colName)
                arcs+= """)</text>\n"""
            else:
                arcs += """<text tool="CPN Tools" version="4.0.1">{}</text>\n""".format(a.expr)
            arcs+="""</annot>\n</arc>\n"""

        xml+=arcs


        xml+="""</page>\n"""

        #instance
        idInstance=Id
        Id+=1
        xml+="""<instances>\n<instance id="ID{}" page="ID{}"/>\n</instances>\n""".format(idInstance,idPage)

        #binder
        idBinder=Id
        Id+=1
        xml+="""<binders>\n"""
        xml+="""<cpnbinder id="ID{}" x="257" y="122" width="600" height="400">\n""".format(idBinder)
        idSheet=Id
        Id+=1
        xml+="""<sheets>\n"""
        xml+="""<cpnsheet id="ID{}" panx="-6.0" pany="-5.0" zoom="1.0" instance="ID{}">\n""".format(idSheet,idInstance)
        xml+="""<zorder>\n<position value="0"/>\n</zorder>\n"""
        xml+="""</cpnsheet>\n</sheets>\n"""
        xml+="""<zorder>\n<position value="0"/>\n</zorder>\n"""
        xml+="""</cpnbinder>\n</binders>\n"""

        #Monitors
        xml+="""<monitorblock name="Monitors"/>\n"""


        #End of xml code
        xml+="""</cpnet>\n</workspaceElements>\n"""

        #create output file
        output=open("./processmining/static/{}.cpn".format(self.cpnName),'w+')
        output.write(xml)





class Place():

    def __init__(self,name,col,mark,number_of_marks,id,resource_list_,composeColor):
        self.placeName=name
        self.placeColor=col
        self.initMarking=mark
        self.id=id
        self.marks = number_of_marks
        self.resource_list = resource_list_
        self.compose_color = composeColor

    def __repr__(self):
        return("{}".format(self.placeName))

    def __str__(self):
        return("Place: {}, {}, initMarking {}".format(self.placeName,self.placeColor,self.initMarking))

    def __eq__(self,other):
        return(self.id==other.id)


class Transition():

    def __init__(self,name,id,origen,destino):
        self.transName=name
        self.id=id
        self.place_orig= origen
        self.place_final = destino
        self.listArcs=[]

    def __repr__(self):
        return(self.transName)

    def __eq__(self,other):
        return(self.id==other.id)

    def addArc(self,arc):
        self.listArcs.append(arc)



class Arc():

    def __init__(self,typ,P,T,exp=''):
    #typ must be PtoT or TtoP
        try:
            if typ=="PtoT" or typ=="TtoP":
                self.type=typ
            else:
                raise ValueError("Wrong Arc type: {}".format(typ))
        except ValueError as ve:
            print(ve)

        self.expr=exp
        self.place=P
        self.trans=T

    def __repr__(self):
        if self.type=='PtoT':
            return("{} from {} to {}, expr={}".format(self.type,self.place.placeName,self.trans.transName,self.expr))
        else:
            return("{} from {} to {}, expr={}".format(self.type,self.trans.transName,self.place.placeName,self.expr))


class Color():

    def __init__(self,name,items,var):
        self.colName=name
        self.colset=items
        self.colVar=var

    def __repr__(self):
        return("Colset {}".format(self.colName))

    def __eq__(self,other):
        return self.colName==other.colName
class ComposedColor ():

    def __init__(self,name,list_of_colors):
        self.colName=name
        self.listaColores = list_of_colors

    def __repr__(self):
        return("Colset {}".format(self.colName))

    def __eq__(self,other):
        return self.colName==other.colName

def create_transitions(list_places,CPN,lastID,list_transitions):

    for key_places in list_transitions:
        origen_destino = key_places.split(";")
        origen = origen_destino[0]
        destino = origen_destino[1]
        orig = CPN.listPlaces[origen]
        dest = CPN.listPlaces[destino]
        new_tr = Transition(orig.placeName+dest.placeName ,lastID,orig,dest)
        CPN.addTransition(new_tr)
        lastID += 1

    orig = list_places[len(list_places)-1]
    dest = list_places[0]
    new_tr = Transition(orig.placeName + dest.placeName, lastID, orig, dest)
    CPN.addTransition(new_tr)
    lastID += 1
    return lastID

def create_arcs(list_transition,CPN):
    lofarcs = []
    for transition in list_transition:
        place_orig_t =transition.place_orig
        place_final_t= transition.place_final
        new_arc_orig = Arc("PtoT",place_orig_t, transition,'paciente')
        new_arc_dest = Arc("TtoP", place_final_t, transition, 'paciente')
        if place_orig_t.resource_list:
            for resource_orig in place_orig_t.resource_list:
                resource_place = CPN.listPlaces[resource_orig.colName]
                new_arc_dest_r = Arc("TtoP", resource_place, transition, resource_place.placeName)
                lofarcs.append(new_arc_dest_r)
                CPN.addArc(new_arc_dest_r)

        if place_final_t.resource_list:
            for resource_dest in place_final_t.resource_list:
                resource_place = CPN.listPlaces[resource_dest.colName]
                new_arc_dest_r = Arc("PtoT", resource_place, transition, resource_place.placeName)
                lofarcs.append(new_arc_dest_r)
                CPN.addArc(new_arc_dest_r)

        lofarcs.append(new_arc_orig)
        lofarcs.append(new_arc_dest)
        CPN.addArc(new_arc_orig)
        CPN.addArc(new_arc_dest)
    return lofarcs

def create_list_recource_colors(list_resources,dict_resources,CPN):

    dict_resources_1 = dict()
    for resource_1 in list_resources:
        new_color = Color(resource_1, [], resource_1)
        dict_resources_1[resource_1] = new_color
        CPN.addColor(new_color)



    new_dict_resource = dict()
    for resource_key in dict_resources.keys():
        new_dict_resource[resource_key]=[]
        for resource_2 in dict_resources[resource_key]:
            new_dict_resource[resource_key].append(dict_resources_1[resource_2])


    return new_dict_resource

def create_composed_color(list_resources,CPN,color_inicial):
    new_name =color_inicial.colName
    for resource in list_resources:
        new_name+=resource.colName
    new_list = list_resources + [color_inicial]
    new_color = ComposedColor(new_name,new_list)
    if not new_color in CPN.composed_color:
        CPN.composed_color.append(new_color)
        return new_color
    else:
       for color in CPN.composed_color:
           if color.colName == new_color.colName:
               return color



def create_CPN(CPN_name, CPN_list_places,CPN_list_resources,CPN_list_transitions,CPN_dict_resources_places):


    test=CPN(CPN_name)
    Id=1
    ################
    #    Data      #
    ################
    #P=['Iniciorp','p2','p3'] #Set of places
    # S = ['Iniciorp;p2', 'p2;p3']
    #Recursos = ['medico', 'enfermera']
    # dict_resources = dict()
    # dict_resources['p2'] = ['medico', 'enfermera']

    P = CPN_list_places
    R=['paciente1','paciente2'] #Set of robots
    S = CPN_list_transitions
    Recursos = CPN_list_resources
    dict_resources = CPN_dict_resources_places



    PACIENTE=Color('paciente',R,'paciente')

    test.addColor(PACIENTE)

    # Create places and colors for resources



    places_resources = create_list_recource_colors(Recursos,dict_resources,test)

    Y=[''] #Set of tasks
    for resource in Recursos:
        newplace = Place(resource, PACIENTE, resource, 0, Id,[],[])
        newplace.marking = newplace.initMarking.replace('`', '*')
        test.addPlace(newplace)
        Id += 1

    #
    ################






    # Add Create new

    List_places= []
    for newP in P:
        if newP in places_resources.keys():
            nuevos_recursos = places_resources[newP]
            new_col = create_composed_color(nuevos_recursos,test,PACIENTE)
            newplace = Place(newP, PACIENTE, 'paciente', 0, Id, places_resources[newP],new_col)
        else:
            newplace = Place(newP, PACIENTE, 'paciente', 0, Id, [],[])

        newplace.marking = newplace.initMarking.replace('`', '*')
        test.addPlace(newplace)
        List_places.append(newplace)
        Id+=1

    Id = create_transitions(List_places,test,Id,S)
    list_arcs= create_arcs(test.listTrans,test)
    test.generateXML(Id)
