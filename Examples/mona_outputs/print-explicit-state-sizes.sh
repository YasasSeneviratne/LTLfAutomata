#!/bin/bash

# The purpose of this script is to go through all of the patterns and MONA-fi the 
# pattern and its reverse as well as capture the number of states produced by the resulting DFA
# This is based on LTLfAutomata/code/make-anml-from-rules.sh

# The one argument is the directory to do this in

pushd $PWD

cd $1

#Extension
ext2="anml_non_min.anml" 
ext="anml_min.anml"
for directory in ./combined_10*/; do
        echo $directory 
        cd $directory

        totalstates=0

        # cd into anml
        cd anml
        echo "DFA Results"
        for file in rule*.${ext}; do
                #echo $file
                num_states=$(~/src/VASim/vasim $file | grep -m 1 Elements:)
                numstates="${num_states#*:}"
                numstates=$((numstates))
                #echo "NumStates:$numstates"
                totalstates=$((totalstates + $numstates))
        done

        echo "Total States:$totalstates"

	totalstates=0
        cd ../ranml
        echo "NFA Results"
        for file in rule*.${ext}; do
                #echo $file
                num_states=$(~/src/VASim/vasim $file | grep -m 1 Elements:)
                numstates="${num_states#*:}"
                numstates=$((numstates))
                #echo "NumStates:$numstates"
                totalstates=$((totalstates + $numstates))
        done

        echo "Total States:$totalstates"

        cd ../..
done

popd
