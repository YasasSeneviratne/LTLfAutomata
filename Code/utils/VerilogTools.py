'''
    The purpose of this tool is to convert our truth-table
    into a Verilog primitive for use within our FPGA code.
'''

def transform_bdd(bdd_data):
    """
    This function transforms bdds into space-separated list of variables
    for a truth-table representation
    """

    # This needs to be implemented
    truth_table_data = bdd_data

    return truth_table_data


def make_primitive(truth_table_data, num_inputs, verilog_output):
    """
    This function generates a TruthTable Verilog user-defined primitive
    """

    # We need to support more than 26 input variables
    assert num_inputs < 24, "Too many input variables!"
    inputs = [chr(ord('a') + i) for i in range(num_inputs)]

    output = 'y'
    verilog_code = "primitive TruthTable ({},{});\n".format(output, ','.join(inputs))
    verilog_code += "\toutput {};\n".format(output)
    verilog_code += "\tinput {};\n".format(','.join(inputs))
    verilog_code += "\ttable\n"
    verilog_code += "\t\t// {} : {}".format(' '.join(inputs), output)

    for line in truth_table_data:
        verilog_code += "\t\t\t{}\n".format(line)
    
    verilog_code += "\tendtable"
    verilog_code += "endprimitive"

    try:
        with open(verilog_output, 'w') as f:
            f.write(verilog_code)
    
    except Exception as e:
        print("Cannot write to file {}".format(verilog_output))
        print("\tException: ", e)
        exit(-1)