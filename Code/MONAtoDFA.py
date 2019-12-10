#!/usr/bin/env python

'''
The purpose of this tool is to parse the output of MONA and generate DFAs for processing with other tools.
Author: Tommy Tracy II
Email: tjt7a@virginia.edu
Date: 9 December 2019
Version: 0.0.1

To generate MONA output:
./mona -w -e <first order logic input file> > <MONA output file>
'''

# Imports
import sys
import re

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./MONAtoDFA.py <MONA input file> <DFA output file>"
    return usage

# Parse the MONA file for automata
def parse_mona(mona_file):
    try:
        with open(mona_file, 'r') as f:
            mona_content = f.readlines()

    except Exception as e:
        print("Cannot open mona file %s".format(mona_file))

    transitions_mode = False
    transition_dict = {}

    # Parse the file from top to bottom
    for line in mona_content:

        if not transitions_mode:

            # Grab the automata details
            if 'DFA for formula with free variables' in line:
                free_variables = line.split(':')[1].strip().split()

            if 'Initial state' in line:
                initial_states = line.split(':')[1].strip().split()

            if 'Accepting states' in line:
                accepting_states = line.split(':')[1].strip().split()

            if 'Rejecting states' in line:
                rejecting_states = line.split(':')[1].strip().split()

            if "Don't-care states" in line:
                done_care_states = line.split(':')[1].strip().split()

            if 'Automaton has' in line:
                num_states, num_bdd_nodes = re.findall(r'[0-9]+', line)

            if 'Transitions:' in line:
                transitions_mode = True

        else:
            if '->' in line:
                left_side, right_side = map(lambda x: x.strip(), line.split('->'))
                destination_state = int(right_side.split()[1].strip())
                source_side, transition_alphabet = map(lambda x: x.strip(), left_side.split(':'))
                source_state = source_side.split()[1].strip()

                if source_state not in transition_dict:
                    transition_dict[source_state] = [(transition_alphabet, destination_state)]
                else:
                    transition_dict[source_state].append((transition_alphabet, destination_state))
            else:
                transition_mode = False



    print("Free Variables: ", free_variables)
    print("Initial State: ", initial_states)
    print("Accepting States: ", accepting_states)
    print("Rejecting States: ", rejecting_states)
    print("Don't Care States: ", done_care_states)
    print("Num States: ", num_states)
    print("Num BDD Nodes: ", num_bdd_nodes)
    print("----------")
    print("")
    print("Transition Dictionary")
    print(transition_dict)




# Entry point
if __name__ == '__main__':

    # Check the correct number of command line arguments
    if len(sys.argv) != 3:
        print(usage())
        exit(-1)

    mona_input = sys.argv[1]
    dfa_output = sys.argv[2]
    parse_mona(mona_input)
