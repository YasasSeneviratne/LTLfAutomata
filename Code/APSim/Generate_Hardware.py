#!/usr/bin/env python2

"""
    The purpose of this script is to convert an ANML file into a full hardware implementation
    for deployment on AWS with APSim.
    !! To use it, you must have APSim installed.
    Install from here: https://github.com/tjt7a/APSim

"""

import automata as atma
import sys, os
import shutil
from automata.utility.utility import minimize_automata
import automata.HDL.hdl_generator as hd_gen
import glob

dbw = None

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./APSim.py <automata symbol bit width> <input ANML file directory> <automata per stage> [--symbolic]"
    return usage

# Process ANML
def process_anml(bitwidth, input_anml_directory, automata_per_stage):

    # This is the directory name to be created for HDL files
    output_hdl_directory = input_anml_directory + '_' + str(bitwidth) + '_' + str(automata_per_stage)

    anml_input_files = glob.glob(input_anml_directory + '/*.anml')
    print "ANML Files: ", anml_input_files

    # Parse the ANML file
    automata = atma.parse_anml_file(anml_input_file)

    # Minimizing the automata with NFA heuristics
    print "Minimizing Automata"
    minimize_automata(automata)

    # Clean up directory
    shutil.rmtree(output_hdl_directory, ignore_errors=True)
    os.mkdir(output_hdl_directory)

    # Create a directory name for the HDL code
    hdl_folder_name = hd_gen.get_hdl_folder_name(prefix=output_hdl_directory, number_of_atms=len(anml_input_files),
                                                stride_value=0, before_match_reg=False,
                                                after_match_reg=False, ste_type=1, use_bram=False,
                                                use_compression=False, compression_depth=-1, symbolic=False)
                    
    print "Folder name to store the HDLs: ", hdl_folder_name

    # Create a hardware Generator
    generator_ins = hd_gen.HDL_Gen(path=os.path.join(output_hdl_directory, hdl_folder_name), before_match_reg=False,
                                   after_match_reg=False, ste_type=1,
                                   total_input_len=dbw, symbolic=False)



    # Iterate through the ANML files in the directory
    for index, anml_input_file in enumerate(anml_input_files):

        # Assign each unique automaton its own unique name or the HDL generator won't work
        automata.id = 'an{}'.format(index)

        # Drawing automata graph
        print "Drawing automata svg graph"
        automata.draw_graph(anml_input_file + "_minimized_hw.svg")

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


def process_truthtable(bitwidth, input_anml_directory, automata_per_stage):

    # This is the directory name to be created for HDL files
    output_hdl_directory = input_anml_directory + '_' + str(bitwidth) + '_' + str(automata_per_stage)

    # Grab the input files
    truthtable_input_files = glob.glob(input_anml_directory + '/*.tt')
    print "Truth Table Files: ", truthtable_input_files

    # Clean up directory
    shutil.rmtree(output_hdl_directory, ignore_errors=True)
    os.mkdir(output_hdl_directory)

    # Create a directory name for the HDL code
    hdl_folder_name = hd_gen.get_hdl_folder_name(prefix=output_hdl_directory, number_of_atms=len(truthtable_input_files),
                                                stride_value=0, before_match_reg=False,
                                                after_match_reg=False, ste_type=1, use_bram=False,
                                                use_compression=False, compression_depth=-1, symbolic=True)
                    
    print "Folder name to store the HDLs: ", hdl_folder_name

    # Create a hardware Generator
    generator_ins = hd_gen.HDL_Gen(path=os.path.join(output_hdl_directory, hdl_folder_name), before_match_reg=False,
                                   after_match_reg=False, ste_type=1,
                                   total_input_len=dbw, symbolic=True)


    # Iterate through the ANML files in the directory
    for index, anml_input_file in enumerate(truthtable_input_files):

        # Assign each unique automaton its own unique name or the HDL generator won't work
        automata.id = 'an{}'.format(index)

        # Drawing automata graph
        print "Drawing automata svg graph"
        automata.draw_graph(anml_input_file + "_minimized_hw.svg")

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


if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) == 4:
        symbolic = False
    elif len(sys.argv) == 5 and sys.argv[4] == "--symbolic":
        symbolic = True
    else:
        print(usage())
        exit(-1)
    
    # Bitwidth of the explicit automata
    if sys.argv[1].isdigit():
        dbw = int(sys.argv[1])
    else:
        print "Error with first argument: {}; should be a positive integer".format(sys.argv[1])
        exit(2)

    # This is the directory that contains the ANML files
    input_anml_directory = sys.argv[2]

    # This is the number of automata set per stage in the pipeline
    if sys.argv[3].isdigit():
        automata_per_stage = int(sys.argv[3])
    else:
        print "Error with third argument: {}; should be a positive integer".format(sys.argv[3])
        exit(2)

    # Process either Truth Tables or ANML files
    if symbolic:
        process_truthtable(bdw, input_anml_directory, automata_per_stage)
    else:
        process_anml(bdw, input_anml_directory, automata_per_stage)