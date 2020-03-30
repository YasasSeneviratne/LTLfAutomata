'''
The purpose of this module is to parse MONA file contents
and translate from signal bit vectors into discrete symbols
'''

import re

# Parse the MONA file for automata
# Symbol sets the transition to symbols instead of bit vectors
def parse_mona(mona_file, translate_table='signal_to_symbol_translation.txt', reverse=False, remove_unreachable=True, verbose=False):
    
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

    # Automaton might have been generated with no don't-care states,
    # so make sure that dont_care_states is declared even if that's the case
    dont_care_states = []

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

    # Removes superfluous state 0 added to the automaton by MONA
    try:
        remove_zero_state(mona_data)
    except ValueError:
        print('Mona File {} does not contain a transition it should'.format(mona_file))

    # Remove unreachable states from the MONA-generated DFA
    if remove_unreachable:
        remove_unreachable_states(mona_data)
    
    # Reverse the automaton if reverse flag was set
    if reverse:
        reverse_automaton(mona_data)
    
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

# Reverse automaton by swapping initial and final states, and reversing transitions
# This might turn a DFA into an NFA
def reverse_automaton(mona_data):
    # Swap initial and accepting states
    mona_data['initial_states'], mona_data['accepting_states'] = mona_data['accepting_states'], mona_data['initial_states']
        
    initial_set = set(mona_data['initial_states'])
    accepting_set = set(mona_data['accepting_states'])
    rejecting_set = set(mona_data['rejecting_states'])
    dont_care_set = set(mona_data['dont_care_states'])
    
    # Previous non-accepting states have become accepting, so remove those
    mona_data['rejecting_states'] = list(rejecting_set - accepting_set)

    # Also add initial states, which used to be accepting, to don't-care set
    # Since we don't differentiate between don't-care and rejecting, the choice of which to make them is arbitrary
    # We follow MONA's convention of making initial states don't-care because it assumes the trace will be non-empty
    mona_data['dont_care_states'] = list((dont_care_set - accepting_set) | initial_set)

    # Reverse all transitions by swapping source and destination
    mona_data['transition_dict'] = {(dest, source): label
                                    for (source, dest), label in mona_data['transition_dict'].items()}

# The initial state 0 in the DFAs generated by MONA is superfluous in our case
# In general, this state is used to read time-independent variables before the trace starts
# Since in our case we don't have time-independent variables, this state should be removed
def remove_zero_state(mona_data):
    try:
        del mona_data['transition_dict'][("0", "1")]
    except KeyError:
        print("Something went wrong; MONA DFA expected to have transition 0 -[X]-> 1")
        raise ValueError
        #exit(-1)

    # After deleting the transition 0 -[X]-> 1, there should be no more transitions from or to state 0
    zero_edges = {(source, dest)
                 for (source, dest) in mona_data['transition_dict'].keys()
                  if source == "0" or dest == "0"}
        
    if zero_edges:
        print("Something went wrong; state 0 expected to have only one transition")
        exit(-1)

    def update_state(state):
        return str(int(state) - 1)
        
    def update_state_set(state_set):
        return {update_state(s) for s in state_set if s != "0"}

    def update_transition_dict(transition_dict):
        return {(update_state(source), update_state(dest)): label
                for (source, dest), label in transition_dict.items()}

    # Remove state 0 and move all other states down by one
    mona_data['states'] = update_state_set(mona_data['states'])
    mona_data['accepting_states'] = update_state_set(mona_data['accepting_states'])
    mona_data['rejecting_states'] = update_state_set(mona_data['rejecting_states'])
    mona_data['dont_care_states'] = update_state_set(mona_data['dont_care_states'])
    mona_data['num_states'] -= 1
    mona_data['transition_dict'] = update_transition_dict(mona_data['transition_dict'])


def remove_unreachable_states(mona_data):
    """
    The purpose of this function is to remove states that cannot reach an accepting/reporting states
    As per MONA's convention, any such states would be rejecting states, and there should only be 
    one of them in an automaton.
    """

    # Remove all cases in the transition dict where the state is either a source or a destination
    def remove_state_from_transition_dict(transition_dict, state):
        return {(source, dest): label
            for (source, dest), label in transition_dict.items()
                if source != state and dest != state}

    states_to_remove = []

    # As per convention, only rejecting states can be unreachable
    for state in mona_data['rejecting_states']:

        # Check if this state cannot reach an accepting/reporting state
        # For now, we assume that only states that are not reporting and have
        # no outgoing (no self-referential) edges, cannot reach reporting
        unreachable = True
        for (source, dest), label in mona_data['transition_dict'].items():
            if source == state and dest != state:
                unreachable = False
        
        # If unreachable, remove the state
        if unreachable:
            states_to_remove.append(state)


    for state in states_to_remove:

        # Remove state from states
        assert state in mona_data['states']
        mona_data['states'].remove(state)

        # Reduce num_states by one
        mona_data['num_states'] -= 1

        # Remove from rejecting states
        assert state in mona_data['rejecting_states']
        mona_data['rejecting_states'].remove(state)

        # Remove all relevant transitions
        mona_data['transition_dict'] = remove_state_from_transition_dict(mona_data['transition_dict'], state)
            
            

