#!/bin/bash

#Comment: This script has been multi-threaded; make sure the below variables are set correctly

threads=10

for num_automata in 10 100 1000 10000
do
    input_dir="../Examples/mona_outputs/combined_${num_automata}"
    anml_dir="../Examples/mona_outputs/combined_${num_automata}/tt"
    ranml_dir="../Examples/mona_outputs/combined_${num_automata}/rtt"

    mkdir -p ${anml_dir}
    mkdir -p ${ranml_dir}

    # The task is responsible for generating truthtable files from out and rout MONA outputs
    task(){
        echo "Running rules from $1 to $2"
        for i in $(eval echo {$1..$2});
        do
            ./MONAtoTruthTable.py ${input_dir}/rule${i}.out ${anml_dir}/rule${i}.tt
            ./MONAtoTruthTable.py ${input_dir}/rule${i}.rout ${ranml_dir}/rule${i}.tt --reverse
        done
    }

    max_thread_id=$((threads - 1))
    # We don't have a ceiling function, so let's use this math trick
    automata_per_thread=$(((num_automata + threads - 1)/threads))

    last_automata=$((num_automata - 1))
    for i in $(eval echo {0..$max_thread_id});
    do
        start=$((i * automata_per_thread))
        end=$((start + automata_per_thread - 1))
        end=$((end>last_automata ? last_automata : end))
        task ${start} ${end} &
    done

    wait
done
