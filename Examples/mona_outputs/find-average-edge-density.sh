#!/bin/bash

# The purpose of this script is to go through all of the patterns and MONA-fi the 
# pattern and its reverse as well as capture the number of states produced by the resulting DFA
# This is based on LTLfAutomata/code/make-anml-from-rules.sh

# The one argument is the directory to do this in

pushd $PWD

cd $1

#Extension
ext="anml"
for directory in ./combined_1000/; do
        echo $directory 
        cd $directory

        totalstates=0
	# This is the total, biased average node degree
	totalaveragenodedegree=0
	counter=0

        # cd into anml
        cd anml
        echo "DFA Results"
        for file in rule*.${ext}; do
                num_states=$(~/src/VASim/vasim $file | grep -m 1 Elements:)
		avg_node_degree=$(~/src/VASim/vasim $file | grep -m 1 Degree:)

                numstates="${num_states#*:}"
                numstates=$((numstates))
                
		avg_node_degree="${avg_node_degree#*:}"

                totalstates=$((totalstates + $numstates))
		sum="scale=2; $totalaveragenodedegree + $numstates * $avg_node_degree"
		totalaveragenodedegree="`bc -l <<< $sum`"

		counter=$((counter + 1))
	done

	division="scale=2; $totalaveragenodedegree / $totalstates"
	netnodedegree="`bc -l <<< $division`"

        echo "Total States:$totalstates"
	echo "Net Node Degree:$netnodedegree"
	echo "Number of Automata:$counter"

	totalstates=0
	totalaveragenodedegree=0
	counter=0


        cd ../ranml
        echo "NFA Results"
        for file in rule*.${ext}; do
                #echo $file
                num_states=$(~/src/VASim/vasim $file | grep -m 1 Elements:)
                avg_node_degree=$(~/src/VASim/vasim $file | grep -m 1 Degree:)

		numstates="${num_states#*:}"
                numstates=$((numstates))
                
		avg_node_degree="${avg_node_degree#*:}"		

		#echo "NumStates:$numstates"
                totalstates=$((totalstates + $numstates))
		sum="$totalaveragenodedegree + $numstates * $avg_node_degree"
                totalaveragenodedegree="`bc -l <<< $sum`"

                counter=$((counter + 1))

        done

        division="scale=2; $totalaveragenodedegree / $totalstates"
        netnodedegree="`bc -l <<< $division`"

        echo "Total States:$totalstates"
        echo "Net Node Degree:$netnodedegree"
        echo "Number of Automata:$counter"



        cd ../..
done

popd
