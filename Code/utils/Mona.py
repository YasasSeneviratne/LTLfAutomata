'''
The purpose of this module is to parse MONA file contents
and translate from signal bit vectors into discrete symbols
'''

import re

# Parse the MONA file for automata
# Symbol sets the transition to symbols instead of bit vectors
def parse_mona(mona_file, translate_table='signal_to_symbol_translation.txt', reverse=False, verbose=False):
    
    # Read the entire MONA File
    mona_content = None
    try:
        with open(mona_file, 'r') as f:
            mona_content = f.readlines()

    # Catch read exception
    except Exception as e:
        print("Cannot open mona file {}".format(mona_file))
        print("\tException: ", e)
        exit(-1)

    translation_list = []
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
                dont_care_states = line.split(':')[1].strip().split()

            if 'Automaton has' in line:
                num_states, num_bdd_nodes = re.findall(r'[0-9]+', line)
                num_states = int(num_states)
                num_bdd_nodes = int(num_bdd_nodes)

            if 'Transitions:' in line:
                transitions_mode = True

        else:

            # Parse the transition information
            if '->' in line:
                left_side, right_side = map(lambda x: x.strip(), line.split('->'))
                destination_state = right_side.split()[1].strip()
                source_side, transition_signal = map(lambda x: x.strip(), left_side.split(':'))
                source_state = source_side.split()[1].strip()

                # If we're reversing the automaton, swap source and destination states
                if reverse:
                    source_state, destination_state = destination_state, source_state
                
                # Translate bit pattern to unique symbol
                transition_alphabet = alphabet(transition_signal)

                # If we're writing a translation table, write to file
                if translate_table:
                    if (transition_signal, transition_alphabet) not in translation_list:
                        translation_list.append((transition_signal, transition_alphabet))

                # Keep track of transition alphabets from source to destination states
                if (source_state, destination_state) not in transition_dict:
                    transition_dict[(source_state, destination_state)] = transition_alphabet
                else:
                    transition_dict[(source_state, destination_state)].extend(transition_alphabet)
            else:
                transitions_mode = False

    # If we're reversing the automaton, swap initial and accepting states
    if reverse:
        initial_states, accepting_states = accepting_states, initial_states
        
        # Previous non-accepting states have become accepting, so remove those
        accepting_set = set(accepting_states)
        rejecting_states = list(set(rejecting_states) - accepting_set)

        # Also add initial states, which used to be accepting, to don't-care set
        dont_care_states = list((set(dont_care_states) - accepting_set) | set(initial_states))
        
    # Collect all the states
    states = set()
    for state in initial_states:
        states.add(state)
    for state in accepting_states:
        states.add(state)
    for state in rejecting_states:
        states.add(state)
    for state in dont_care_states:
        states.add(state)

    states = list(states)

    assert (len(states) == num_states), "We're missing states!"

    # Dump some information about the parsed MONA file
    mona_data = {
            'free_variables': free_variables, 
            'states': states,
            'initial_states': initial_states,
            'accepting_states': accepting_states,
            'rejecting_states': rejecting_states,
            'dont_care_states': dont_care_states,
            'num_states': num_states,
            'transition_dict': transition_dict
            }
    
    # Print the parsed data for debugging
    if verbose:
        print("Parsed MONA DFA Information")
        for k, v in mona_data.items():
            print('\t' + str(k) + ": " + str(v))

    # Populate the translation table
    if translate_table:

        try:
            translate_table_file = open(translate_table, 'w')
            translate_table_file.write("MONA Signals\t:\tEquivalent Symbols\n")
            translate_table_file.write("------------------------------------------\n")

            for (transition_signal, transition_alphabet) in translation_list:
                translate_table_file.write("{}\t\t:\t{}\n".format(transition_signal, transition_alphabet))

        except Exception as e:
            print("Cannot write to translate table file {}".format(translate_table))
            print("Exception: ", e)

        translate_table_file.close()

    return mona_data

# Generate character set from the MONA signal representation
# I'm assuming the signals are all binary, requiring 2^variable unique symbols
def alphabet(mona_data):

    # Function for translating bit pattern into unique symbol, or symbols
    # In the case that there is an X in the bit vector, multiple symbols will
    # correspond to the accepted character set
    def symbol(input_bits):

        # Start off with one symbol
        partial_sums = [0]
        buffer = []

        # Go through the bit vector and convert to a symbol value
        for i, v in enumerate(input_bits[::-1]):
            
            # Don't-Cares accept multiple values
            if v == 'X':

                # For each value in our partial sums
                for partial_sum in partial_sums:

                    # Append the case where the X is a 1, and when it is a 0
                    buffer.append((partial_sum + 2**i))
                    buffer.append(partial_sum)
            
            # If not an X, add the next partial sum
            else:

                for partial_sum in partial_sums:

                    buffer.append(partial_sum + ((2**i) * int(v)))
                
            # Update partial_sums list and empty buffer
            partial_sums = buffer
            buffer = []
        
        # We are going to remove duplicates with the set cast
        # Then make sure that the symbols are sorted
        partial_sums = list(set(partial_sums))
        partial_sums.sort()
            
        return partial_sums

    return symbol(mona_data)
