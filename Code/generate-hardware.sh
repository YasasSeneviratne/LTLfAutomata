#!/bin/bash

# This script is responsible for generating HDL hardware for explicit automata (ANML and RANML) and truth tables (TTs and RTTs)
# It has one argument which is the symbol bit width:
#      - Symbol bit Width: 8


if [ $# -ne 1 ] ; then echo "Arguments expected: <Symbol Bit Width>" ; exit; fi


symbol_bit_width=$(($1))

for num_automata in 10 100 1000 10000
do
    echo "Generating ${automata} automata"

    anml_dir="../Examples/mona_outputs/combined_${num_automata}/anml"
    ranml_dir="../Examples/mona_outputs/combined_${num_automata}/ranml"
    tt_dir="../Examples/mona_outputs/combined_${num_automata}/tt"
    rtt_dir="../Examples/mona_outputs/combined_${num_automata}/rtt"

    explicittask(){
        echo "Running Explicit Hardware Generator"
        rm -fr $2/*explicit*
        rm -f $2/*.zip
        ~/src/LTLfAutomata/Code/APSim/Generate_Hardware.py $1 $2 $3
    }

    symbolictask(){
        echo "Running Symbolic Hardware Generator"
        rm -fr $2/*symbolic*
        rm -f $2/*.zip
        ~/src/LTLfAutomata/Code/APSim/Generate_Hardware.py $1 $2 $3 --symbolic
    }

    explicittask ${symbol_bit_width} ${anml_dir} ${num_automata} &
    explicittask ${symbol_bit_width} ${ranml_dir} ${num_automata} &

    symbolictask ${symbol_bit_width} ${tt_dir} ${num_automata} &
    symbolictask ${symbol_bit_width} ${rtt_dir} ${num_automata} &

    wait
    echo "Done running Harware Generators"

done
