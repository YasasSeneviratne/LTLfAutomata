#!/usr/bin/env python3

'''
The purpose of this tool is to parse the output of MONA and generate DFAs for processing with other tools.
Author: Tommy Tracy II
Email: tjt7a@virginia.edu
Date: 9 December 2019
**Under Development**

To generate MONA output:
./mona -w -e <first order logic input file> > <MONA output file>
'''

# Imports
import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import to_agraph
from utils import PlotDFA
from utils import Mona
from utils import AutomataTools


# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./MONAtoDFA.py <MONA input file> <DFA output file> [--reverse]"
    return usage

# Entry point
if __name__ == '__main__':

    verbose = False
    
    # Check the correct number of command line arguments
    if len(sys.argv) == 3:
        reverse = False
    elif len(sys.argv) == 4 and sys.argv[3] == "--reverse":
        reverse = True
    else:
        print(usage())
        exit(-1)

    # Grab the input and output filenames
    mona_input = sys.argv[1] # This is the output from the MONA program
    homogeneous_output = sys.argv[2] # This is the homogeneous output

    # Parse the mona file
    mona_data = Mona.parse_mona(mona_input, reverse=reverse, verbose=verbose)

    # Generate a graph SVG file to visualize the DFA after removing unreachable 
    if verbose:
        PlotDFA.generate_graph(mona_data['transition_dict'], mona_data['initial_states'], mona_data['accepting_states'], "{}.svg".format(mona_input), verbose=verbose)

    # Translate non-homogeneous automata into homogeneous automata

    # ADDED: We need to have ANML files with differing automata names
    # to do this, we're going to use the filename of the mona input to name our automata
    assert '.' in mona_input, "We expect the mona_input file ({}) to contain a .out or .rout".format(mona_input)
    if '/' in mona_input:
        filename = mona_input.split('/')[-1]
    else:
        filename = mona_input
    automata_name = filename.split('.')[0]
    #print(automata_name)
    AutomataTools.make_homogeneous(mona_data, homogeneous_output, aId=automata_name)
