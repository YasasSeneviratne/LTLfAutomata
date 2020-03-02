#!/usr/bin/env python2

'''
    ! This script requires APSim to be installed !
    The purpose of this script is to:
    1. load an ANML automata file
    2. draw its non-minimized version (_non_min.svg)
    3. minimize the automata
    4. draw its minimized version (_min.svg)
'''

import automata as atma
import sys, os
import shutil
from automata.utility.utility import minimize_automata
import automata.HDL.hdl_generator as hd_gen
from multiprocessing.dummy import Pool as ThreadPool

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./Minimize_and_homogenize.py <input ANML file>"
    return usage

if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) != 2:
        print(usage())
        exit(-1)

    # This is the directory that contains the ANML files
    anml_input_file = sys.argv[1]
    print "ANML Input File: ", anml_input_file

    # Parse the ANML file
    automata = atma.parse_anml_file(anml_input_file)

    # Drawing automata before minimizing
    print "Drawing non-minimized automata svg graph"
    print automata.get_summary(logo=" of the homogeneous, automata")
    automata.draw_graph(anml_input_file + "_non_min.svg")
    atma.generate_anml_file(anml_input_file + "_non_min.anml", automata)

    print "The automata {} homogeneous!".format('is' if automata.is_homogeneous else 'is not')

    print "Minimizing Automata"
    minimize_automata(automata)
    print automata.get_summary(logo=" of the homogeneous, minimized, automata")

    # Drawing automata graph
    print "Drawing automata svg graph"
    automata.draw_graph(anml_input_file + "_min.svg")

    atma.generate_anml_file(anml_input_file + "_min.anml", automata)
