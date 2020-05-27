#!/usr/bin/env python3

from utils import Mona
import sys

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./count_mona_states.py <MONA input file>"
    return usage

# Entry point
if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) != 2:
        print(usage())
        exit(-1)

    # Grab the input and output filenames
    mona_input = sys.argv[1] # This is the output from the MONA program
 
    # Parse the mona file
    mona_data = Mona.parse_mona(mona_input, reverse=False, verbose=False)
    print(mona_data['num_states'])
