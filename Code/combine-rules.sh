#!/bin/bash

number_of_rules=100
number_of_patterns_per_rule=10
number_of_vars=10

input_dir="../Examples/mona_inputs/patterns"
output_dir="../Examples/mona_inputs/combined"
dfa_dir="../Examples/mona_outputs/combined"

mkdir -p ${output_dir}
mkdir -p ${dfa_dir}

# All files in this format will be used as candidate patterns to sample from
input_format="${input_dir}/*/*.fol"
# Combined formulas and automata will be in this format, with %d replaced by numbers between 0 and number_of_rules - 1
output_format="${output_dir}/rule%d.fol"
dfa_format="${dfa_dir}/rule%d.out"

seed=${RANDOM}

echo "Generating rules (random seed: ${seed})..."

python3 CombineRules.py ${seed} ${number_of_rules} ${number_of_patterns_per_rule} ${number_of_vars} ${output_format} ${input_format}

echo "Constructing DFAs..."

for i in $(seq 0 $((number_of_rules - 1)))
do
    echo "DFA for rule ${i}..."
    output_file=$(printf "${output_format}" ${i})
    dfa_file=$(printf "${dfa_format}" ${i})
    mona -xw -u ${output_file} > ${dfa_file}
done

echo "Done!"

