#!/usr/bin/env python2

import automata as atma
import sys, os
import shutil
from automata.utility.utility import minimize_automata
import automata.HDL.hdl_generator as hd_gen
from multiprocessing.dummy import Pool as ThreadPool
import glob

out_dir_prefix = './'
dbw = 4

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./APSim.py <input ANML directory> <output HDL directory>"
    return usage


if __name__ == '__main__':
    
    # Check the correct number of command line arguments
    if len(sys.argv) != 3:
        print(usage())
        exit(-1)
    
    # ANML directory
    input_anml_directory = sys.argv[1]
    output_hdl_directory = sys.argv[2]

    anml_input_files = glob.glob(input_anml_directory + '/*.anml')

    # Clean up directory
    shutil.rmtree(output_hdl_directory, ignore_errors=True)
    os.mkdir(output_hdl_directory)

    # Create a directory name for the HDL code
    hdl_folder_name = hd_gen.get_hdl_folder_name(prefix='temp', number_of_atms=len(anml_input_files),
                                                stride_value=0, before_match_reg=False,
                                                after_match_reg=False, ste_type=1, use_bram=False,
                                                use_compression=False, compression_depth=-1)
                    
    print("Folder name to store the HDLs: ", hdl_folder_name)

    generator_ins = hd_gen.HDL_Gen(path=os.path.join(output_hdl_directory, hdl_folder_name), before_match_reg=False,
                                   after_match_reg=False, ste_type=1,
                                   total_input_len=dbw)

    # Iterate through the ANML files in the directory
    for index, anml_input_file in enumerate(anml_input_files):

        # Parse the ANML file
        automata = atma.parse_anml_file(anml_input_file)

        # Assign each unique automaton its own unique name or the HDL generator won't work
        automata.id = 'an{}'.format(index)

        # Convert to homogeneous and minimized form
        automata.make_homogenous()
        minimize_automata(automata)

        print(automata.get_summary(logo=" of the homogeneous, minimized, automata"))

        # Convert to a dbw-bitwidth automaton
        b_atm = atma.automata_network.get_bit_automaton(automata, original_bit_width=automata.max_val_dim_bits_len)
        automata = atma.automata_network.get_strided_automata2(atm=b_atm,
                                                      stride_value=dbw,
                                                      is_scalar=True,
                                                      base_value=2,
                                                      add_residual=True)
        automata.make_homogenous()
        minimize_automata(automata)
        generator_ins.register_automata(atm=automata, use_compression=False)

    # Once all of the automata have been registered, add registers
    generator_ins.register_stage_pending(single_out=False, use_bram=False)

    #Finalize and wrap up HDL in archive folder
    generator_ins.finilize()
    shutil.make_archive(hdl_folder_name, 'zip', output_hdl_directory)
    shutil.rmtree(output_hdl_directory)