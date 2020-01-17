'''
The purpose of this module is to plot the DFA parsed from the MONA file
'''

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph 


# Generate a graph from the transitions
def generate_graph(transitions, filename):

    G = nx.MultiDiGraph()

    # Add an edge from state src to state dest with transition_alphabet edge label
    for (src, dest), transition_alphabet in transitions.items():
        G.add_edge(src, dest, label=transition_alphabet)

    # Generate a SVG file depicting the graph
    A = to_agraph(G) 
    A.layout('dot')                                                                 
    A.draw(filename) 
