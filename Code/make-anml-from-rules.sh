#!/bin/bash

input_dir="../Examples/mona_outputs/combined"
anml_dir="../Examples/mona_outputs/combined/anml"

mkdir -p ${anml_dir}

for i in {0..99}
do
    ./MONAtoDFA.py ${input_dir}/rule${i}.out ${anml_dir}/rule${i}.anml
done
