#!/bin/bash

number_of_rules=1000000
number_of_vars=100

input_dir="../Examples/mona_outputs/patterns"
output_dir="../Examples/mona_outputs/combined"

mkdir -p ${output_dir}

seed=${RANDOM}

echo "Generating rules (random seed: ${seed})..."

python3 CombineRules.py ${seed} ${number_of_rules} ${number_of_vars} ${output_dir} ${input_dir}/*/*.out

echo "Done!"

