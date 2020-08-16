#!/bin/bash

# The one argument is the directory to do this in

pushd $PWD

cd $1

for directory in ./combined_10*/; do
        echo $directory 
        cd $directory

        # cd into anml
        cd anml
        echo "Minimize DFAs"
        for file in rule*.anml; do
                #echo $file
        	/home/tjt7a/src/LTLfAutomata/Code/APSim/Minimize.py $file
	done


        cd ../ranml
        echo "Minimize NFAs"
        for file in rule*.anml; do
                #echo $file
        	/home/tjt7a/src/LTLfAutomata/Code/APSim/Minimize.py $file
	done

        cd ../..
done

popd
