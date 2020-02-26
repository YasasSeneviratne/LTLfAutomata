#!/bin/bash

number_of_rules=1000000
number_of_vars=100

input_dir="../Examples/mona_inputs"
output_dir="../Examples/mona_inputs/combined"
dfa_dir="../Examples/mona_outputs/combined"

mkdir -p ${output_dir}
mkdir -p ${dfa_dir}

seed=${RANDOM}

echo "Generating rules (random seed: ${seed})..."

python3 CombineRules.py ${seed} ${number_of_rules} ${number_of_vars} ${output_dir} ${input_dir}/*.fol

echo "Done!"

echo "Converting rules to automata..."

for i in $(seq 0 $(( ${number_of_rules} - 1 )))
do
    echo "Generating automaton ${i}"
    mona -w ${output_dir}/rule${i}.fol > ${dfa_dir}/rule${i}.out
done
