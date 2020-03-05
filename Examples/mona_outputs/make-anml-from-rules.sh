#!/bin/bash

# The purpose of this script is to go through all of the patterns and MONA-fi the 
# pattern and its reverse as well as capture the number of states produced by the resulting DFA
# This is based on LTLfAutomata/code/make-anml-from-rules.sh

for directory in ./patterns/*/; do
	echo $directory	
	cd $directory
	rm *.anml *.txt *.svg *num_states
	for file in *.out; do 	
		~/src/LTLfAutomata/Code/MONAtoDFA.py $file $file.anml | grep num_states > $file.num_states
		echo $file
		cat $file.num_states
	done
	for file in *.rout; do 	
		~/src/LTLfAutomata/Code/MONAtoDFA.py $file $file.anml --reverse | grep num_states > $file.num_states
		echo $file
		cat $file.num_states
	done
	cd ../..
done
