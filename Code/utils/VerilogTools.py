'''
    The purpose of this tool is to convert our truth-table
    into a Verilog primitive for use within our FPGA code.
'''

from enum import Enum

# def transform_bdd(bdd_data):
#     """
#     This function transforms bdds into space-separated list of variables
#     for a truth-table representation
#     """

#     # This needs to be implemented
#     truth_table_data = bdd_data

#     return truth_table_data


def read_truth_table_file(truth_table_file):
    """
    This function reads a truth table file
    and returns a list of string for each line
    """

    file_content = None

    # Open the truth table file and read
    with open(truth_table_file, 'r') as f:
        file_content = f.readlines()
    
    return file_content


class TruthTableType(Enum):
    REPORTING = 1
    TRANSITION = 2

class TruthTable:
    """
        This class encapsulates one truth table
    """
    def __init__(self, type, header):
        """
            Initialize a TruthTable object with a type and header
        """
        self.type = type
        self.header = header
        self.transitions = []
    
    def add_transition(self, transition):
        """
            Adds a transition to our Truth Table
        """
        self.transitions.append(transition)
    
    def __str__(self):
        """
            ToString() for our TruthTable class
        """
        return_string = "Truth Table type="
        return_string += 'REPORTING' if self.type == TruthTableType.REPORTING else 'TRANSITION'
        return_string += '\n'
        for k,v in self.header.items():
            if k not in ['next_state', 'output']:
                return_string += '[' + k + '=' + ','.join(v) + ']'
            else:
                return_string += '[' + k + '=' + v + ']'
        return_string += '\n'
        return_string += '--------------------------------------\n'
        for transition_dict in self.transitions:
            for k,v in transition_dict.items():
                return_string += '[' + k + '=' + ','.join(v) + ']'
            return_string += '\n'
        return return_string


def parse_truth_tables(truth_table_data):
    """
        This function breaks the data into multiple
        truth tables to be passed to verilog generator
    """

    results = []
    tt = None
    header = True
    transitions = []

    # Go through each line
    for line in truth_table_data:
        
        # We found an empty line, which means the next
        # non-empty line is a header (or EOF)
        if not line.strip():

            # If we have valid transitions from the previous
            # truth table, add them to our list
            if len(tt.transitions) > 0:
                results.append(tt)
            header = True
            continue

        # We're in header mode
        if header:

            # Take each colon-separated header and strip off newlines and spaces
            headers = list(map(lambda x: x.strip(), line.split(':')))

            inputs = list(map(lambda x: x.strip(), headers[0].split()))

            # If we only have two header sections, this is a reporting table
            #            section 0                   section 1
            # new_state_bit_0 new_state_bit_1 ... : report
            if len(headers) == 2:
                output = headers[1].strip()
                assert output == 'report', "Output signal is not called 'report'!"
                tt = TruthTable(TruthTableType.REPORTING, 
                                {
                                    'inputs': inputs,
                                    'output': output}
                                )
            
            # Else, it must be a state-transition table, and therefore have 3 header sections
            #             section 0                section 1                 section 2
            # input_bit_0 input_bit_1 ... : old_state_0 old_state_1 ... : new_state_bit
            else:
                assert len(headers) == 3, "Cannot parse this line: {}".format(line)
                previous_state = list(map(lambda x: x.strip(), headers[1].split()))
                next_state = headers[2].strip()
                tt = TruthTable(TruthTableType.TRANSITION,
                                {
                                    'inputs': inputs,
                                    'previous_state': previous_state,
                                    'next_state': next_state
                                }
                            )

            # We're done with the header; start a new transitions list
            header = False
            transitions = []
        
        else:
            transition = list(map(lambda x: x.strip(), line.split(':')))

            inputs = list(map(lambda x: x.strip(), transition[0].split()))

            if tt.type == TruthTableType.TRANSITION:
                previous_state = list(map(lambda x: x.strip(), transition[1].split()))
                next_state = transition[2].strip()
                
                tt.add_transition({
                    'inputs': inputs,
                    'previous_state': previous_state,
                    'next_state': next_state
                })
            else:
                output = transition[1].strip()

                tt.add_transition({
                    'inputs': inputs,
                    'output': output
                })

    if len(transitions) > 0:
        results.append(tt)
    
    return results


def build_primitive_truthtable(truth_table_file, output_verilog_file):
    """
    This function parses a truth table (.tt) file and generates
    custom primitive truthtable files.
    """

    # Read in truth table data generated by Lucas's script
    data = read_truth_table_file(truth_table_file)
    truth_tables = parse_truth_tables(data)

    for truth_table in truth_tables:
        print(truth_table)

    verilog_code = ""

    for truth_table in truth_tables:
        if truth_table.type == TruthTableType.REPORTING:
            verilog_code += make_combinationatorial_udp(truth_table)

        elif truth_table.type == TruthTableType.TRANSITION:
            verilog_code += make_sequential_udp(truth_table)
        else:
            raise Exception('Unsupported truth table type: {}'.format(truth_table.type))
        
        #Add a newline between tables
        verilog_code += "\n"

    try:
        with open(output_verilog_file, 'w') as f:
            f.write(verilog_code)
    
    except Exception as e:
        print("Cannot write to file {}".format(output_verilog_file))
        print("\tException: ", e)
        exit(-1)


def make_combinationatorial_udp(truth_table):
    """
    This function generates a TruthTable Verilog user-defined primitive
    This is only used for the reporting truthtable, which is combinatorial
    """

    output = truth_table.header['output']
    inputs = truth_table.header['inputs']
    transitions = truth_table.transitions

    verilog_code = "primitive {}TruthTable ({},{});\n".format(output, output, ','.join(inputs))
    verilog_code += "\toutput {};\n".format(output)
    verilog_code += "\tinput {};\n".format(','.join(inputs))
    verilog_code += "\ttable\n"
    verilog_code += "\t\t// {} : {}\n".format(' '.join(inputs), output)

    for transition in transitions:
        inputs = transition['inputs']
        output = transition['output']
        verilog_code += "\t\t{} : {};\n".format(' '.join(inputs), output)
    verilog_code += '\n'
    verilog_code += "\tendtable\n"
    verilog_code += "endprimitive\n"
    verilog_code += '\n'

    return verilog_code

def transform_old_to_new(old_signal):
    """
    This helper function simply replaces 'old' in a signal name with 'new'
    """


def make_sequential_udp(truth_table):
    """
    This function generates a TruthTable Verilog user-definied primitive
    This is used for state transition logic, which is sequential
    """

    inputs = truth_table.header['inputs']
    previous_states = truth_table.header['previous_state']
    next_state = truth_table.header['next_state']

    # This is a little tricky
    # If we have more than one bit in the previous_state
    # We need to take all other bits and consider those inputs
    # from other truth tables
    assert 'new' in next_state, 'Next State not properly named: {}'.format(next_state)

    # This is one of the previous state signals
    previous_state = next_state.replace('new', 'old')

    # Make sure that the naming convention is followed
    assert previous_state in previous_states, 'State names are not properly named: {}'.format(previous_state)
    
    # We'll use the index of the previous state and remove it below
    previous_state_index = previous_states.index(previous_state)

    # Now remove our one previous state signal from the remaining
    previous_states.remove(previous_state)

    # Replace all the other signals with 'new'; they'll be inputs from other TTs
    input_state_bits = []
    for state in previous_states:
        input_state = state.replace('old', 'new')
        input_state_bits.append(input_state)

    # Add all of the new state bits to our inputs list
    inputs.extend(input_state_bits)

    transitions = truth_table.transitions

    verilog_code = "primitive {}TruthTable ({}, {}, clk, rst);\n".format(next_state, next_state, ','.join(inputs))
    verilog_code += "\tinput clk, rst, {};\n".format(','.join(inputs))
    verilog_code += "\toutput {};\n".format(next_state)
    verilog_code += "\treg {};\n".format(next_state)
    verilog_code += "\tinitial\n"
    verilog_code += "\t{} = 1'b1;\n\n".format(next_state)
    verilog_code += "\ttable\n"
    verilog_code += "\t\t// {} clk rst : {} : {}\n".format(' '.join(inputs), previous_state, next_state)

    # This first transition line is for the reset
    verilog_code += "\t\t {} ? 1: ? : 0;\n".format(' '.join(['?' for x in inputs]))

    for transition in transitions:
        inputs = transition['inputs']
        previous_states = transition['previous_state']
        next_state = transition['next_state']

        for i,state in enumerate(previous_states):
            if i != previous_state_index:
                inputs.append(state)
            else:
                previous_state = state

        verilog_code += "\t\t{} R 0: {} : {};\n".format(' '.join(inputs), previous_state, next_state)

    verilog_code += "\tendtable\n"
    verilog_code += "endprimitive\n\n"
    verilog_code += '\n'

    return verilog_code


def make_module():
    """
    This function generates the module interface for the symbolic
    finite state automaton.
    """

    verilog_code = "module TransitionTable(q, clk, reset"
    verilog_code += "input clk, reset, "
    verilog_code += "output report;\n"


    verilog_code += "endmodule\n"

    return verilog_code


if __name__ == '__main__':
    build_primitive_truthtable('/home/tjt7a/src/LTLfAutomata/Examples/truth_tables/response.tt', 'output.v')