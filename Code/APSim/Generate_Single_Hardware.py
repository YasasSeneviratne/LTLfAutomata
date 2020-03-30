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
from multiprocessing.dummy import Pool as ThreadPool
import glob

dbw = None

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./APSim.py <automata symbol bit width> <input ANML file> <number of automata>"
    return usage


if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) != 4:
        print(usage())
        exit(-1)
    
    # Bitwidth of the explicit automata
    dbw = int(sys.argv[1])

    # This is the directory that contains the ANML files
    input_anml_file = sys.argv[2]

    # This is the directory name to be created for HDL files
    num_automata = int(sys.argv[3])

    output_hdl_directory = input_anml_file + '_' + str(num_automata)

    # Clean up directory
    shutil.rmtree(output_hdl_directory, ignore_errors=True)
    os.mkdir(output_hdl_directory)

    # Create a directory name for the HDL code
    hdl_folder_name = hd_gen.get_hdl_folder_name(prefix=input_anml_file, number_of_atms=num_automata,
                                                stride_value=1, before_match_reg=False,
                                                after_match_reg=False, ste_type=1, use_bram=False,
                                                use_compression=False, compression_depth=-1)
                    
    #print "Folder name to store the HDLs: ", hdl_folder_name

    # Create a hardware Generator
    generator_ins = hd_gen.HDL_Gen(path=os.path.join(output_hdl_directory, hdl_folder_name), before_match_reg=False,
                                   after_match_reg=False, ste_type=1,
                                   total_input_len=dbw)


    #print "ANML Input File: ", input_anml_file

    # Parse the ANML file
    automata = atma.parse_anml_file(input_anml_file)

    # Iterate through the ANML files in the directory
    for index in range(num_automata):

        temp_automata = automata.clone()

        # Assign each unique automaton its own unique name or the HDL generator won't work
        temp_automata.id = 'an{}'.format(index)

        generator_ins.register_automata(atm=temp_automata, use_compression=False)

    # Once all of the automata have been registered, add registers
    generator_ins.register_stage_pending(single_out=False, use_bram=False)

    #Finalize and wrap up HDL in archive folder
    generator_ins.finilize()
    # Changed 'zip' to 'gztar' because of the 2GB limit of zip
    shutil.make_archive(hdl_folder_name, 'gztar', output_hdl_directory)
    shutil.rmtree(output_hdl_directory)
