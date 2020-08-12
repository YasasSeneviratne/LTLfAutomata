#!/usr/bin/env python2

'''
    ! This script requires APSim to be installed !
    Install my fork:
    https://github.com/tjt7a/APSim

    The purpose of this script is to:
    1. load an ANML automata file
'''

import automata as atma
import sys, os
import shutil
from automata.utility.utility import minimize_automata
import automata.HDL.hdl_generator as hd_gen

minimize = True

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./Generate_tt.py <input ANML file> <output verilog file>"
    return usage

if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) != 3:
        print(usage())
        exit(-1)

    # This is the input ANML File
    anml_input_file = sys.argv[1]

    # This is the output System Verilog File
    verilog_output_file = sys.argv[2]

    # Parse the ANML file
    automata = atma.parse_anml_file(anml_input_file)

    # If we want to minimize the automata
    if minimize:
        minimize_automata(automata)

    tables, start_states, accept_states = atma.generate_tt(automata)

    # print "Start States: ", start_states
    # print "---------------"
    # for state, table in tables['transition'].items():
    #     print state
    #     for row in table:
    #         print row
    # print "---------------"       
    # print "---------------"
    # print "Accept States: ", accept_states
    # exit()

    atma.build_truthtable(tables, start_states, accept_states, 'testing', verilog_output_file)
