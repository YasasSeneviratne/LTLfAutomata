#!/usr/bin/env python3

'''
The purpose of this tool is to parse the output of MONA, encode the automaton
in binary and generate truth tables for its transition function
Author: Lucas M. Tabajara
Email: lucasmt@rice.edu
Date: 5 February 2020
**Under Development**

To generate MONA output:
./mona -w -e <first order logic input file> > <MONA output file>
'''

# Imports
import sys
from utils import Mona
from utils import TruthTable


# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./MONAtoDFA.py <MONA input file> <TT output file> [--reverse]"
    return usage

# Entry point
if __name__ == '__main__':

    verbose = True
    
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
    truth_table_output = sys.argv[2] # This is the truth table output

    # Parse the mona file
    mona_data = Mona.parse_mona(mona_input, reverse=reverse, verbose=verbose)
    
    # Generate the truth tables
    if reverse:
        tables = TruthTable.from_nfa(mona_data)
    else:
        tables = TruthTable.from_dfa(mona_data)

    # Save tables to file
    TruthTable.save_to_file(tables, truth_table_output)
