#!/usr/bin/env python3

'''
The purpose of this tool is to parse BDDs and convert them into Truth Tables for use with VERILOG
Author: Tommy Tracy II
Email: tjt7a@virginia.edu
Date: 3 February 2020
**Under Development**
'''

# Imports
import sys
from utils import Mona
from utils import VerilogTools


# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./BDDtoVERILOG <BDD Representation> > <Verilog output file>"
    return usage

# Entry point
if __name__ == '__main__':

    verbose = True

    # Check the correct number of command line arguments
    if len(sys.argv) != 3:
        print(usage())
        exit(-1)

    # Grab the input and output filenames
    bdd_input = sys.argv[1] # This is the BDD output
    verilog_output = sys.argv[2] # This is the verilog output

    # Parse the BDD file
    bdd_data = Mona.parse_bdd(bdd_input, verbose=verbose)

    # Convert BDD representation into verilog primitive truth table
    VerilogTools.make_primitive(bdd_data, verilog_output)
