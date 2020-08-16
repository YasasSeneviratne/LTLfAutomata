#!/bin/bash

# This script is responsible for zipping up our HDL Verilog and sending it to AWS nodes where it will be synthesized and place/routed
# The single argument for this script is the bit-width of the design
#     - bitwidth: The bitwidth of the automata design; for these experiments this number is always 8
# IMPORTANT NOTE: It is important to set all of the target IP addresses below to valid EC2 instances with F1 AFI
# Also make sure that you have the correct directory structure on the target instance so the SCP is successful

if [ $# -ne 1 ] ; then echo "Arguments expected: <number of variables>" ; exit; fi

# Important: set the IP Addresses to each target to parallelize
target1="34.235.26.149" # for dfas
target2="34.235.26.149" #for tts
target3="54.90.126.237" #for rtts
target4="54.84.210.184" #for nfas

number_of_vars=$(($1))

for num_automata in 100 100 1000 10000
do
    echo "Deploying ${automata} automata"

    anml_dir="../Examples/mona_outputs/10vars_disjunct/5_vars/run_2/combined_${num_automata}/anml"
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
