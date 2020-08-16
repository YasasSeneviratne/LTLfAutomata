#!/bin/bash


#Extension
dfaext="out" 
nfaext="rout"


for directory in $1; do
        echo $directory 
        cd $directory

        totaldfastates=0

        # cd into anml
        echo "DFA Results"
        for file in rule*.${dfaext}; do
		#echo "Filename: $file"
                num_states=$(~/src/LTLfAutomata/Code/count_symbolic_states.py $file)
                #echo "DFA Num States: $num_states"
		numstates=$((num_states))
                totaldfastates=$((totaldfastates + $numstates))
        done

	totalnfastates=0
        echo "NFA Results"
        for file in rule*.${nfaext}; do
		#echo "Filename: $file"
		num_states=$(~/src/LTLfAutomata/Code/count_symbolic_states.py $file)
                #echo "NFA Num States: $num_states"
		numstates=$((num_states))
                totalnfastates=$((totalnfastates + $numstates))
        done

	echo "Total DFA States:$totaldfastates"
	echo "Total NFA States:$totalnfastates"

done

