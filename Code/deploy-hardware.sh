#!/bin/bash

target1="18.208.225.41"
target2="34.235.26.149"

for num_automata in 10 100 1000 10000
do
    echo "Generating ${automata} automata"

    anml_dir="../Examples/mona_outputs/combined_${num_automata}/anml"
    ranml_dir="../ranml"
    tt_dir="../tt"
    rtt_dir="../rtt"

    cd ${anml_dir}
    zip -r ${num_automata}.zip 10_*
    scp -i ~/Documents/aws/AWS_Automata_RTL.pem ${num_automata}.zip centos@${target1}:~/Downloads/dfas/.

    cd ${ranml_dir}
    zip -r ${num_automata}.zip 10_*
    scp -i ~/Documents/aws/AWS_Automata_RTL.pem ${num_automata}.zip centos@${target1}:~/Downloads/nfas/.

    cd ${tt_dir}
    zip -r ${num_automata}.zip 10_*
    scp -i ~/Documents/aws/AWS_Automata_RTL.pem ${num_automata}.zip centos@${target2}:~/Downloads/tts/.

    cd ${rtt_dir}
    zip -r ${num_automata}.zip 10_*
    scp -i ~/Documents/aws/AWS_Automata_RTL.pem ${num_automata}.zip centos@${target2}:~/Downloads/rtts/.

    cd ../../../../Code

done
