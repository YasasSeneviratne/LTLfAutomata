#!/bin/bash

number_of_rules=100
number_of_patterns_per_rule=3
number_of_vars=10

input_dir="../Examples/mona_inputs/patterns"
output_dir="../Examples/mona_inputs/combined"
dfa_dir="../Examples/mona_outputs/combined"

mkdir -p ${output_dir}
mkdir -p ${dfa_dir}

# All files in this format will be used as candidate patterns to sample from
input_prefix="${input_dir}/*/*"
input_format="${input_prefix}.fol"
reverse_input_format="${input_prefix}.rfol"

# Combined formulas and automata will be in this format, with %d replaced by numbers between 0 and number_of_rules - 1
output_prefix="${output_dir}/rule%d"
output_format="${output_prefix}.fol"
reverse_output_format="${output_prefix}.rfol"

log_format="${output_prefix}.log"
reverse_log_format="${output_prefix}.rlog"

dfa_prefix="${dfa_dir}/rule%d"
dfa_format="${dfa_prefix}.out"
reverse_dfa_format="${dfa_prefix}.rout"

seed=${RANDOM}

echo "Generating rules (random seed: ${seed})..."

python3 CombineRules.py ${seed} ${number_of_rules} ${number_of_patterns_per_rule} ${number_of_vars} ${output_format} ${log_format} ${input_format}

python3 CombineRules.py ${seed} ${number_of_rules} ${number_of_patterns_per_rule} ${number_of_vars} ${reverse_output_format} ${reverse_log_format} ${reverse_input_format}

echo "Checking diffs between logs (all diffs should be empty)..."

for i in $(seq 0 $((number_of_rules - 1)))
do
    echo "Log for rule ${i}..."
    log_file=$(printf "${log_format}" ${i})
    reverse_log_file=$(printf "${reverse_log_format}" ${i})
    diff ${log_file} ${reverse_log_file}
done

echo "Constructing DFAs..."

for i in $(seq 0 $((number_of_rules - 1)))
do
    echo "DFA for rule ${i}..."
    output_file=$(printf "${output_format}" ${i})
    dfa_file=$(printf "${dfa_format}" ${i})
    mona -xw -u ${output_file} > ${dfa_file}

    echo "Reverse DFA for rule ${i}..."
    reverse_output_file=$(printf "${reverse_output_format}" ${i})
    reverse_dfa_file=$(printf "${reverse_dfa_format}" ${i})
    mona -xw -u ${reverse_output_file} > ${reverse_dfa_file}
done

echo "Done!"

