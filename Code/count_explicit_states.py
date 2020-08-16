#!/usr/bin/env python2

import automata as atma
from utils import Mona
import sys
from automata.utility.utility import minimize_automata


# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./count_explicit_states.py <ANML File>"
    return usage

# Entry point
if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) != 2:
        print(usage())
        exit(-1)

    # Grab the input filename
    anml_input = sys.argv[1]
 
    # Parse the ANML file
    automata = atma.parse_anml_file(anml_input)
    before = automata.nodes_count

    # Minimizing the automata with NFA heuristics
    minimize_automata(automata)

    after = automata.nodes_count

    print(str(before) + ", " + str(after))
