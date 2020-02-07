#!/bin/bash

input_dir="../Examples/mona_inputs"
output_dir="../Examples/mona_inputs/combined"
dfa_dir="../Examples/mona_outputs/combined"

mkdir -p ${output_dir}
mkdir -p ${dfa_dir}

python3 CombineRules.py ${input_dir} 100 10 ${output_dir}

for i in {0..99}
do
    mona -w ${output_dir}/rule${i}.fol > ${dfa_dir}/rule${i}.out
done
