#!/bin/bash

# This script is responsible for generating HDL hardware for explicit automata (ANML and RANML) and truth tables (TTs and RTTs)
# It has one argument which is the symbol bit width:
#      - Symbol bit Width: 8


if [ $# -ne 3 ] ; then echo "Arguments expected: <path to anml and tt dirs> <Symbol Bit Width> <# of input files>" ; exit; fi


symbol_bit_width=$(($2))

echo "Generating ${automata} automata"

anml_dir="$1/anml"
ranml_dir="$1/ranml"
tt_dir="$1/tt"
rtt_dir="$1/rtt"
num_automata=$3

explicittask(){
    echo "Running Explicit Hardware Generator"
    rm -fr $2/*explicit*
    rm -f $2/*.zip
    /home/yasas/Research/RTLruntimemonitor/APSim/Examples/Generate_Hardware.py $1 $2 $3
}

symbolictask(){
    echo "Running Symbolic Hardware Generator"
    rm -fr $2/*symbolic*
    rm -f $2/*.zip
    /home/yasas/Research/RTLruntimemonitor/APSim/Examples/Generate_Hardware.py $1 $2 $3 --symbolic
}

explicittask ${symbol_bit_width} ${anml_dir} ${num_automata} &
explicittask ${symbol_bit_width} ${ranml_dir} ${num_automata} &

#symbolictask ${symbol_bit_width} ${tt_dir} ${num_automata} &
#symbolictask ${symbol_bit_width} ${rtt_dir} ${num_automata} &

wait
echo "Done running Harware Generators"


