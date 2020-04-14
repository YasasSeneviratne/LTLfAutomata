#!/bin/bash

symbol_bit_width=100

for num_automata in 10 100 1000 10000
do
    echo "Generating ${automata} automata"

    anml_dir="../Examples/mona_outputs/combined_${num_automata}/anml"
    ranml_dir="../Examples/mona_outputs/combined_${num_automata}/ranml"
    tt_dir="../Examples/mona_outputs/combined_${num_automata}/tt"
    rtt_dir="../Examples/mona_outputs/combined_${num_automata}/rtt"

    explicittask(){
        echo "Running Explicit Hardware Generator"
        ~/src/LTLfAutomata/Code/APSim/Generate_Hardware.py $1 $2 $3
    }

    symbolictask(){
        echo "Running Symbolic Hardware Generator"
        ~/src/LTLfAutomata/Code/APSim/Generate_Hardware.py $1 $2 $3 --symbolic
    }

    explicittask ${symbol_bit_width} ${anml_dir} ${num_automata} &
    explicittask ${symbol_bit_width} ${ranml_dir} ${num_automata} &

    symbolictask ${symbol_bit_width} ${tt_dir} ${num_automata} &
    symbolictask ${symbol_bit_width} ${rtt_dir} ${num_automata} &

    wait
    echo "Done running Harware Generators"

done
