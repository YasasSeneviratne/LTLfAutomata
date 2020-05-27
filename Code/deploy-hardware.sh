#!/bin/bash

if [ $# -ne 1 ] ; then echo "Arguments expected: <number of variables>" ; exit; fi

# Important: set the IP Addresses to each target to parallelize
target1="54.91.92.124" # for dfas
target2="34.235.26.149" #for tts
target3="3.84.179.238" #for rtts
target4="54.242.102.31" #for nfas

number_of_vars=$(($1))

for num_automata in 10 100 1000 10000
do
    echo "Deploying ${automata} automata"

    anml_dir="../Examples/mona_outputs/combined_${num_automata}/anml"
    ranml_dir="../ranml"
    tt_dir="../tt"
    rtt_dir="../rtt"

    cd ${anml_dir}
    zip -r ${num_automata}.zip ${number_of_vars}_*
    scp -i ~/Documents/aws/AWS_Automata_RTL.pem ${num_automata}.zip centos@${target1}:~/Downloads/dfas/.

    cd ${ranml_dir}
    zip -r ${num_automata}.zip ${number_of_vars}_*
    scp -i ~/Documents/aws/AWS_Automata_RTL.pem ${num_automata}.zip centos@${target4}:~/Downloads/nfas/.

    cd ${tt_dir}
    zip -r ${num_automata}.zip ${number_of_vars}_*
    scp -i ~/Documents/aws/AWS_Automata_RTL.pem ${num_automata}.zip centos@${target2}:~/Downloads/tts/.

    cd ${rtt_dir}
    zip -r ${num_automata}.zip ${number_of_vars}_*
    scp -i ~/Documents/aws/AWS_Automata_RTL.pem ${num_automata}.zip centos@${target3}:~/Downloads/rtts/.

    cd ../../../../Code

done
