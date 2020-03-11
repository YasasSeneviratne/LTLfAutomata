#!/bin/bash

# The purpose of this script is to go through all of the patterns and MONA-fi the 
# pattern and its reverse as well as capture the number of states produced by the resulting DFA
# This is based on LTLfAutomata/code/make-anml-from-rules.sh

for directory in ./patterns/*/; do
	# Move into pattern directory
	cd $directory
	# Delete old junk
	rm -f *.anml *.txt *.svg *num_states *.zip *.tar.gz
	for file in *.out; do 	
		# Automatize and grab number of states in non-homogeneous
		#~/src/LTLfAutomata/Code/MONAtoDFA.py $file $file.anml | grep num_states > $file.nh.num_states
		nhnumstates=$(cat $file.nh.num_states)
		nhnumstates="${nhnumstates#*:}"
		# Get number of state transition elements in homogeneous version
		hnumstates=$(~/src/VASim/vasim $file.anml | grep -m 1 Elements:)
		hnumstates="${hnumstates#*:}"
		# Get number of states from minimized homogenous version
		#python ~/src/LTLfAutomata/Code/APSim/Minimize_and_homogenize.py $file.anml
		mhnumstates=$(~/src/VASim/vasim $file.anml_min.anml | grep -m 1 Elements:)
		mhnumstates="${mhnumstates#*:}"
		# Get number of signals
		numsignals=$(cat $file | grep "DFA for formula with free variables:")
		numsignals="${numsignals#*:}"
		numsignals=$(echo $numsignals | wc -w)
		echo $file, $nhnumstates, $hnumstates, $mhnumstates, $numsignals

		# Generate hardware
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 1
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 10
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 100
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 1000
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 10000
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 100000
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 1000000
	done
	for file in *.rout; do 	
		# Automatize and grab number of states in non-homogeneous
		#~/src/LTLfAutomata/Code/MONAtoDFA.py $file $file.anml --reverse | grep num_states > $file.nh.num_states
		nhnumstates=$(cat $file.nh.num_states)
		nhnumstates="${nhnumstates#*:}"
		# Get number of state transition elements in homogeneous version
		hnumstates=$(~/src/VASim/vasim $file.anml | grep -m 1 Elements:)
		hnumstates="${hnumstates#*:}"
		# Get number of states from minimized homogenous version
		#python ~/src/LTLfAutomata/Code/APSim/Minimize_and_homogenize.py $file.anml
		mhnumstates=$(~/src/VASim/vasim $file.anml_min.anml | grep -m 1 Elements:)
		mhnumstates="${mhnumstates#*:}"
		# Get number of signals
		numsignals=$(cat $file | grep "DFA for formula with free variables:")
		numsignals="${numsignals#*:}"
		numsignals=$(echo $numsignals | wc -w)
		echo $file, $nhnumstates, $hnumstates, $mhnumstates, $numsignals

		# Generate hardware
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 1
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 10
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 100
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 1000
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 10000
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 100000
		#~/src/LTLfAutomata/Code/APSim/Generate_Single_Hardware.py $numsignals $file.anml_min.anml 1000000
	done
	cd ../..
done
