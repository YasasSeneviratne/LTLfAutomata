#!/bin/bash

# The purpose of this script is to go through all of the patterns and MONA-fi the 
# pattern and its reverse as well as capture the number of states produced by the resulting DFA
# This is based on LTLfAutomata/code/make-anml-from-rules.sh

for directory in ./patterns/*/; do
	echo $directory	
	cd $directory
	for file in *.num_states; do 	
		echo $file
		cat $file
	done
	cd ../..
done
