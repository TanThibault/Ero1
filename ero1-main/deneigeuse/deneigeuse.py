from itineraire import parcours_den,length_boucle,eulerize,length_path

import osmnx as ox
import networkx as nx
import time
import collections
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import sys
from pyomo.environ import *
O = ox.graph_from_place(sys.argv[1]+', Montreal, Canada', network_type='drive')

P = O.subgraph(max(nx.strongly_connected_components(O),key=len))
h = eulerize(P)
d = [u for u, v in nx.eulerian_circuit(h)]

long = length_path(d,O) / 1000

temps_de_travail = 8 
vitesse_type_1 = 10 
vitesse_type_2 = 20 
cout_fixe_type_1 = 500 
cout_fixe_type_2 = 800 
cout_kilometrique_type_1 = 1.1 
cout_kilometrique_type_2 = 1.3 
cout_horaire_lt_8h_type_1 = 1.1 
cout_horaire_lt_8h_type_2 = 1.3 
cout_horaire_ht_8h_type_1 = 1.3 
cout_horaire_ht_8h_type_2 = 1.5 
model = ConcreteModel() 
model.type1 = Var(domain=NonNegativeIntegers) 
model.type2 = Var(domain=NonNegativeIntegers) 
model.distance_type1 = Var(domain=NonNegativeReals) 
model.distance_type2 = Var(domain=NonNegativeReals) 
model.cout = Objective(expr = (cout_fixe_type_1 * model.type1 + cout_fixe_type_2 * model.type2) + (cout_kilometrique_type_1 * model.distance_type1) +(cout_kilometrique_type_2 * model.distance_type2)+(cout_horaire_lt_8h_type_1 * model.distance_type1 / vitesse_type_1) +(cout_horaire_lt_8h_type_2 * model.distance_type2 / vitesse_type_2), sense=minimize)
model.distance_parcourue = Constraint(expr = model.distance_type1 + model.distance_type2 >= long) 
model.totaldistance_type1 = Constraint(expr = vitesse_type_1 * 8 * model.type1 == model.distance_type1) 
model.totaldistance_type2 = Constraint(expr = vitesse_type_2 * 8 * model.type2 == model.distance_type2)
results = SolverFactory('glpk').solve(model) 
if(model.type2()!= 0):
	l,_,_ = length_boucle(h,[],d,model.type1(),model.type2())
else:
	l,_,_ = length_boucle(h,[],d,model.type1(),model.type2())
for i in parcours_den(l,int(model.type1()),int(model.type2())):
	print(i)

print("Le cout de deneigement du bout de quartier est "+str(model.cout())+"$")
