'''
    The purpose of this function is to convert our non-homogeneous
    FSA to a homogeneous FSA for ANML conversion.

    This is a port of Kevin Angstadt's implementation found here:
    https://gist.github.com/kevinaangstadt/727252ac84e8c6a15146703ebedd21a3
'''

from utils.ANML import Anml

# A function for converting between tuples and a
# character class string
def symbol_tuple_to_character_class(symbol_tuple):

    character_class = '['
    for symbol in symbol_tuple:
        character_class += r"\x%02X" % symbol
    character_class += ']'
    return character_class


# A function for converting between non-homogeneous
# and homogeneous automata
def make_homogeneous(mona_data, filename, aId='an1', start_on_all=True):

    ste_count = 0

    # Create an Automata network
    anml = Anml.Anml(aId=aId)

    # Grab details about the DFA
    states = mona_data['states']
    starting_states = mona_data['initial_states']
    accepting_states = mona_data['accepting_states']
    
    # Each non-homogeneous state can map to multiple homogeneous states
    anml_states = {}

    # Create a mapping from non-homogeneous states to their homogeneous counterparts
    for state in states:
        anml_states[state] = dict()

    # Add all of the states
    for (src, dest), symbols in mona_data['transition_dict'].items():

        # Turn symbol lists into set and then tuple to not have to deal with potential 
        # duplication or bad ordering, and then make it hashable
        symbol_tuple = tuple(set(symbols))

        # We need to create a new state representing the transition
        # Only make a new state if there isn't already one for this transition
        if symbol_tuple not in anml_states[dest]:

            if src in starting_states:
                if start_on_all:
                    starting = Anml.AnmlDefs.ALL_INPUT
                else:
                    starting = Anml.AnmlDefs.START_OF_DATA
            else:
                starting = Anml.AnmlDefs.NO_START
            
            if dest in accepting_states:
                accepting = True
                
                # For now, let's just report with a 1
                report_code = 1
            else:
                accepting = False
                report_code = None

            anmlId = '{}-{}'.format(dest, ste_count)
            ste_count += 1

            # create a new state and add it to the ANML network
            # Map the destination non-homo state to the 
            anml_states[dest][symbol_tuple] = anml.AddSTE(symbol_tuple_to_character_class(symbol_tuple), starting, anmlId=anmlId, match=accepting, reportCode=report_code)
        
        # else, trim, because we don't need an extra state (implicit)
    
    # Add transitions to the states
    for (src, dest), symbols in mona_data['transition_dict'].items():

        for (symbol_tuple), dest_ste in anml_states[dest].items():

            # If we're considering the same transition
            if symbol_tuple == tuple(set(symbols)):

                # Go through each of the homogeneous states that the src is represented
                # by, and link them all to this dest state
                for (symbol_tuple), src_ste in anml_states[src].items():

                    anml.AddAnmlEdge(src_ste, dest_ste, 0)
    
    # Pop out the ANML!
    anml.ExportAnml(filename)
