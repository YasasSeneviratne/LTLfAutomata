#!/usr/bin/env python2

import automata as atma
import sys, os
import shutil
from automata.utility.utility import minimize_automata
import automata.HDL.hdl_generator as hd_gen
from multiprocessing.dummy import Pool as ThreadPool

out_dir_prefix = './'
dbw = 4

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./APSim.py <input ANML>"
    return usage


def generate_hardware(atm):

    return_result = {}
    result_dir = out_dir_prefix + str(atm)

    # Clean up directory
    shutil.rmtree(result_dir, ignore_errors=True)
    os.mkdir(result_dir)

    # Create a diectory name for the HDL code
    hdl_folder_name = hd_gen.get_hdl_folder_name(prefix=str(atm), number_of_atms=1,
                                                 stride_value=0, before_match_reg=False,
                                                 after_match_reg=False, ste_type=1, use_bram=False,
                                                 use_compression=False, compression_depth=-1)
    
    print("Folder name to store the HDLs: ", hdl_folder_name)

    generator_ins = hd_gen.HDL_Gen(path=os.path.join(result_dir, hdl_folder_name), before_match_reg=False,
                                   after_match_reg=False, ste_type=1,
                                   total_input_len=dbw)
    
    b_atm = atma.automata_network.get_bit_automaton(atm, original_bit_width=atm.max_val_dim_bits_len)
    atm = atma.automata_network.get_strided_automata2(atm=b_atm,
                                                      stride_value=dbw,
                                                      is_scalar=True,
                                                      base_value=2,
                                                      add_residual=True)
    atm.make_homogenous(plus_src=True)
    minimize_automata(atm)

    generator_ins.register_automata(atm=atm, use_compression=False)

    generator_ins.register_stage_pending(single_out=False, use_bram=False)

    generator_ins.finilize()
    shutil.make_archive(hdl_folder_name, 'zip', result_dir)
    shutil.rmtree(result_dir)


if __name__ == '__main__':
    
    verbose = True

    # Check the correct number of command line arguments
    if len(sys.argv) != 3:
        print(usage())
        exit(-1)
    
    # ANML input file
    anml_input_file = sys.argv[1]

    # Parse the ANML file
    automatas = atma.parse_anml_file(anml_input_file)

    automatas.draw_graph("original_non_homo.svg")

    automatas.make_homogenous(plus_src=True)
    #automatas = automatas.get_single_stride_graph()

    automatas.draw_graph("original_homo.svg")

    minimize_automata(automatas)

    print(automatas.get_summary(logo=" of the homogeneous, minimized, automata"))

    automatas.draw_graph("original_homo_min.svg")

    generate_hardware(automatas)
