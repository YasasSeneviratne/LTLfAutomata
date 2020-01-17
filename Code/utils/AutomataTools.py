'''
    The purpose of this function is to convert our non-homogeneous
    FSA to a homogeneous FSA for ANML conversion.

    This is a port of Kevin Angstadt's implementation found here:
    https://gist.github.com/kevinaangstadt/727252ac84e8c6a15146703ebedd21a3
'''

from utils.ANML import Anml

def make_homogeneous(mona_data):

    # Create a thing
    anml = Anml.Anml()
    stes = []

    num_states = 0

    # Grab details about the DFA
    states = mona_data['states']
    starting_states = mona_data['initial_states']
    accepting_states = mona_data['accepting_states']
    
    # Each non-homogeneous state can map to multiple homogeneous states
    anml_states = {}

    # Create a mapping from non-homogeneous states to their homogeneous counterparts
    for state in states:
        anml_states[state] = []
    
    character_class_lookup = {}

    # Add all of the states
    for (src, dest), symbols in mona_data['transition_dict'].items():

        character_class = '['
        for symbol in symbols:
            character_class += r"\x%02X" % symbol
        character_class += ']'

        # If destination state not in the character_class_lookup dict,
        # Add with empty list of character_class
        if dest not in character_class_lookup:
            character_class_lookup[dest] = []

        # We need to create a new state representing the transition
        # Only make a new state if there isn't already one for this transition
        if character_class not in character_class_lookup[dest]:

            # Store the character_class for the destination
            character_class_lookup[dest].append(character_class)

            if src in starting_states:
                starting = Anml.AnmlDefs.ALL_INPUT
            else:
                starting = Anml.AnmlDefs.NO_START
            
            if dest in accepting_states:
                accepting = True
                # For now, let's just report with a 1
                report_code = 1
            else:
                accepting = False
                report_code = 0

            anmlId = '{}-{}'.format(dest, character_class)

            # create a new state and add it to the ANML network
            ste = anml.AddSTE(character_class, starting, anmlId=anmlId, match=accepting, reportCode=report_code)
            
            # Map the destination non-homo state to the 
            anml_states[dest].append(ste)
        
        # else, trim, because we don't need an extra state (implicit)
    
    # Add transitions to the states
    for (src, dest), symbols in mona_data['transition_dict'].items():

        for ste_src in anml_states[src]:

            for ste_dest in anml_states[dest]:

                anml.AddAnmlEdge(ste_src, ste_dest, 0)
    
    # Pop out the ANML!
    anml.ExportAnml("homogeneous_automata.anml")