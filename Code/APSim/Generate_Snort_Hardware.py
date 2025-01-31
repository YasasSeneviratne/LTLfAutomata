#!/usr/bin/env python2

"""
    The purpose of this script is to convert a directory of ANML files
     or Truth Table files into a full hardware implementation for 
     deployment on AWS with APSim/Grapefruit.
    !! To use it, you must have APSim installed.
    Install from here: https://github.com/tjt7a/APSim

"""

import automata as atma
import sys, os
import shutil
from automata.utility.utility import minimize_automata
import automata.HDL.hdl_generator as hd_gen
import glob
from utils import VerilogTools
from automata import Automatanetwork
from automata.elemnts.ste import S_T_E
from automata.elemnts.element import StartType


dbw = None
minimize = False
drawing = False

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./APSim.py <automata symbol bit width> <input file directory (ANML or Truth Table)> <automata per stage> [--symbolic] [--minimize]\n"
    usage += "\tautomata symbol bit width: number of input variables\n"
    usage += "\tinput file directory: the directory that contains the automata ANML or Truth Table Files\n"
    usage += "\tautomata per stage: designate number of automata per pipeline stage\n"
    usage += "\t--symbolic: This flag allows for symbolic automata construction from truth tables\n"
    return usage

# Process ANML : these are necessarily Homogeneous finite state automata
def process_anml(bitwidth, input_directory, automata_per_stage):

    # This is the directory name to be created for HDL files
    output_hdl_directory = input_directory + '/' + str(bitwidth) + '_' + str(automata_per_stage)

    anml_input_files = glob.glob(input_directory + '/*.anml')
    print("ANML Files: ", anml_input_files)

    # Clean up directory
    shutil.rmtree(output_hdl_directory, ignore_errors=True)
    os.mkdir(output_hdl_directory)

    SYMBOLIC = True

    # Create a directory name for the HDL code
    hdl_folder_name = hd_gen.get_hdl_folder_name(prefix=output_hdl_directory, number_of_atms=len(anml_input_files),
                                                stride_value=0, before_match_reg=False,
                                                after_match_reg=False, ste_type=1, use_bram=False,
                                                use_compression=False, compression_depth=-1, symbolic=SYMBOLIC)
                    
    print("Folder name to store the HDLs: ", hdl_folder_name)

    # Create a hardware Generator
    generator_ins = hd_gen.HDL_Gen(path=hdl_folder_name, before_match_reg=False,
                                   after_match_reg=False, ste_type=1,
                                   total_input_len=dbw, symbolic=SYMBOLIC)



    # Iterate through the ANML files in the directory
    for index, anml_input_file in enumerate(anml_input_files):

        print("Parsing Automata: {}".format(anml_input_file))

        module_name = 'Automata_tt_' + str(index)
        verilog_filename = hdl_folder_name + '/automata_tt_' + str(index) + '.sv'
        
        # Parse the ANML file
        automata = atma.parse_anml_file(anml_input_file)

        # Minimizing the automata with NFA heuristics

        if minimize:
            print("Minimizing Automata: {}".format(anml_input_file))
            minimize_automata(automata)
            #atma.generate_anml_file(anml_input_file + "_min.anml", automata)
        else:
            print("No minimization of Automata")
        
        tables, start_states, accept_states = atma.generate_tt(automata)

        inputs = atma.build_truthtable(tables, start_states, accept_states, module_name, verilog_filename)

        print "Inputs: ", inputs

        # for now, we will use this automata proxy
        automata = Automatanetwork('tt_'+str(index), True, 1, 255, inputs=inputs)

        new_node = S_T_E(start_type=StartType.non_start,
                    is_report=True,
                    is_marked=False,
                    id=automata.get_new_id(),
                    symbol_set=None,
                    adjacent_S_T_E_s=None,
                    report_residual=1,
                    report_code=1)
        
        automata.add_element(new_node)

        print "Number of states: ", automata.nodes_count
        

        # Register this automaton
        generator_ins.register_automata(atm=automata, use_compression=False)

        # We've got another batch of automata_per_stage automata to stage
        if (index + 1) % automata_per_stage == 0:
            generator_ins.register_stage_pending(single_out=False, use_bram=False)

    # DO we need this? maybe if our number of automata is not a perfect multiple
    # of automata_per_stage?
    generator_ins.register_stage_pending(single_out=False, use_bram=False)

    #Finalize and wrap up HDL in archive folder
    generator_ins.finilize()

    # Using gztar to handle LARGE automata workloads
    shutil.make_archive(hdl_folder_name, 'gztar', output_hdl_directory)
    shutil.rmtree(output_hdl_directory)


def process_truthtable(bitwidth, input_directory, automata_per_stage):


    # This is the directory name to be created for HDL files
    output_hdl_directory = input_directory + '/' + str(bitwidth) + '_' + str(automata_per_stage)

    # Grab the input files
    truthtable_input_files = glob.glob(input_directory + '/*.tt')
    print("Truth Table Files: ", truthtable_input_files)

    # Clean up directory
    shutil.rmtree(output_hdl_directory, ignore_errors=True)
    os.mkdir(output_hdl_directory)

    # Create a directory name for the HDL code
    hdl_folder_name = hd_gen.get_hdl_folder_name(prefix=output_hdl_directory, number_of_atms=len(truthtable_input_files),
                                                stride_value=0, before_match_reg=False,
                                                after_match_reg=False, ste_type=1, use_bram=False,
                                                use_compression=False, compression_depth=-1, symbolic=True)
                    
    print("Folder name to store the HDLs: ", hdl_folder_name)

    # Create a hardware Generator
    # for now, we'll only allow either symbolic or explicit automata; no mixing
    generator_ins = hd_gen.HDL_Gen(path=hdl_folder_name, before_match_reg=False,
                                   after_match_reg=False, ste_type=1,
                                   total_input_len=dbw, symbolic=True)


    # Iterate through the TruthTable files in the directory
    for index, truth_table_input_file in enumerate(truthtable_input_files):
 
        # Build a Truthtable module with VerilogTools
        module_name = 'Automata_tt_' + str(index)
        verilog_filename = hdl_folder_name + '/automata_tt_' + str(index) + '.sv'

        print(truth_table_input_file, module_name, verilog_filename)

        inputs = VerilogTools.build_truthtable(truth_table_input_file, module_name, verilog_filename)

        print("Inputs: ", inputs)

        # for now, we will use this automata proxy
        automata = Automatanetwork('tt_'+str(index), True, 1, 255, inputs=inputs)

        new_node = S_T_E(start_type=StartType.non_start,
                    is_report=True,
                    is_marked=False,
                    id=automata.get_new_id(),
                    symbol_set=None,
                    adjacent_S_T_E_s=None,
                    report_residual=1,
                    report_code=1)
        
        automata.add_element(new_node)

        # Register this automaton
        # For now, this just builds the stages
        generator_ins.register_automata(atm=automata, use_compression=False)

        # We've got another batch of automata_per_stage automata to stage
        if (index + 1) % automata_per_stage == 0:
            generator_ins.register_stage_pending(single_out=False, use_bram=False)

    # DO we need this? maybe if our number of automata is not a perfect multiple
    # of automata_per_stage?
    generator_ins.register_stage_pending(single_out=False, use_bram=False)

    #Finalize and wrap up HDL in archive folder
    generator_ins.finilize()

    # Using gztar to handle LARGE automata workloads
    shutil.make_archive(hdl_folder_name, 'gztar', output_hdl_directory)
    shutil.rmtree(output_hdl_directory)


# Entry point of the hardware generator
if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) == 4:
        symbolic = False
    # We now support symbolic automata hardware generation
    elif len(sys.argv) == 5 and sys.argv[4] == "--symbolic":
        symbolic = True
    else:
        print(usage())
        exit(1)
    
    # Bitwidth of the explicit automata
    if sys.argv[1].isdigit():
        dbw = int(sys.argv[1])
    else:
        print("Error with first argument: {}; should be a positive integer".format(sys.argv[1]))
        exit(2)

    # This is the directory that contains the ANML or Truthtable files
    input_directory = sys.argv[2]

    # This is the number of automata set per stage in the pipeline
    if sys.argv[3].isdigit():
        automata_per_stage = int(sys.argv[3])
    else:
        print("Error with third argument: {}; should be a positive integer".format(sys.argv[3]))
        exit(2)

    # Process either Truth Tables or ANML files
    if symbolic:
        process_truthtable(dbw, input_directory, automata_per_stage)
    else:
        process_anml(dbw, input_directory, automata_per_stage)
