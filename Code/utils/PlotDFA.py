'''
The purpose of this module is to plot the DFA parsed from the MONA file
and generate an output SVG file.
'''

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph 


# Generate a graph from the transitions
def generate_graph(transitions, initial_states, accepting_states, filename, verbose=False):

    G = nx.MultiDiGraph()

    # Add an edge from state src to state dest with transition_alphabet edge label
    for (src, dest), transition_alphabet in transitions.items():
        if not G.has_node(src):

            # Make starting states green
            if src in initial_states:
                G.add_node(src, color='green')
            else:     
                G.add_node(src)

        if not G.has_node(dest):

            # Make accepting states red
            if dest in accepting_states:
                G.add_node(dest, color='red')
            else:
                G.add_node(dest)
        G.add_edge(src, dest, label=transition_alphabet)

    # Generate a SVG file depicting the graph
    A = to_agraph(G)
    A.layout('dot')

    if verbose:
        print("Writing out MONA-generated automaton to file: {}".format(filename))

    A.draw(filename)
