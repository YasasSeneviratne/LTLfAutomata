#!/usr/bin/env python2

"""
    The purpose of this script is to convert an ANML file into a full hardware implementation
    for deployment on AWS with APSim.
    !! To use it, you must have APSim installed.

"""

import automata as atma
import sys, os
import shutil
from automata.utility.utility import minimize_automata
import automata.HDL.hdl_generator as hd_gen
from multiprocessing.dummy import Pool as ThreadPool
import glob

dbw = None

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./APSim.py <automata symbol bit width> <input ANML directory> <output HDL directory>"
    return usage


if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) != 4:
        print(usage())
        exit(-1)
    
    # Bitwidth of the explicit automata
    dbw = int(sys.argv[1])

    # This is the directory that contains the ANML files
    input_anml_directory = sys.argv[2]

    # This is the directory name to be created for HDL files
    output_hdl_directory = sys.argv[3]

    anml_input_files = glob.glob(input_anml_directory + '/*.anml')

    print "input files: ", anml_input_files

    # Clean up directory
    shutil.rmtree(output_hdl_directory, ignore_errors=True)
    os.mkdir(output_hdl_directory)

    # Create a directory name for the HDL code
    hdl_folder_name = hd_gen.get_hdl_folder_name(prefix='temp', number_of_atms=len(anml_input_files),
                                                stride_value=dbw, before_match_reg=False,
                                                after_match_reg=False, ste_type=1, use_bram=False,
                                                use_compression=False, compression_depth=-1)
                    
    print "Folder name to store the HDLs: ", hdl_folder_name

    # Create a hardware Generator
    generator_ins = hd_gen.HDL_Gen(path=os.path.join(output_hdl_directory, hdl_folder_name), before_match_reg=False,
                                   after_match_reg=False, ste_type=1,
                                   total_input_len=dbw)

    # Iterate through the ANML files in the directory
    for index, anml_input_file in enumerate(anml_input_files):

        print "ANML Input File: ", anml_input_file

        # Parse the ANML file
        automata = atma.parse_anml_file(anml_input_file)

        # Assign each unique automaton its own unique name or the HDL generator won't work
        automata.id = 'an{}'.format(index)

        print "The automata {} homogeneous!".format('is' if automata.is_homogeneous else 'is not')

        if not automata.is_homogeneous:
            print "Making automata homogeneous"
            
            # Convert to homogeneous and minimized form
            automata.make_homogenous()

        print "Minimizing Automata"
        print automata.get_summary(logo=" of the homogeneous, automata")
        minimize_automata(automata)
        print automata.get_summary(logo=" of the homogeneous, minimized, automata")

        # Convert to a dbw-bitwidth automaton
        # b_atm = atma.automata_network.get_bit_automaton(automata, original_bit_width=automata.max_val_dim_bits_len)
        # automata = atma.automata_network.get_strided_automata2(atm=b_atm,
        #                                               stride_value=dbw,
        #                                               is_scalar=True,
        #                                               base_value=2,
        #                                               add_residual=True)
        # automata.make_homogenous()
        # minimize_automata(automata)

        # Drawing automata graph
        print "Drawing automata svg graph"
        automata.draw_graph(anml_input_file + "_minimized_HW.svg")

        generator_ins.register_automata(atm=automata, use_compression=False)

    # Once all of the automata have been registered, add registers
    generator_ins.register_stage_pending(single_out=False, use_bram=False)

    #Finalize and wrap up HDL in archive folder
    generator_ins.finilize()
    shutil.make_archive(hdl_folder_name, 'zip', output_hdl_directory)
    shutil.rmtree(output_hdl_directory)