#!/usr/bin/env python3

'''
The purpose of this tool is to combine separate rules by merging their variables
Author: Lucas M. Tabajara
Email: lucasmt@rice.edu
Date: 6 February 2020
**Under Development**
'''

# Imports
import os
import sys
import random
import re

# Get the usage string
def usage():
    usage = "----------------- Usage ----------------\n"
    usage += "./CombineRules.py <operator> <random seed> <number of rules> <number of patterns per rule> <number of variables> <output format> <log format> <dfa format> *<pattern files>"
    return usage

def generate_rule(samples, new_vars, output_file, log_file, operator):
    vars_used = set()
    conjuncts = []
    
    with open(log_file, 'w') as log:
        for rule_file in samples:
            with open(rule_file, 'r') as file:
                line = file.readline()

                while line and not line.startswith("var2"):
                    line = file.readline()

                # line is the list of variables

                # remove trailing whitespace and semicolon, then split on spaces and discard first token ("var2")
                old_vars = line.rstrip().rstrip(";").replace(",", "").split(" ")[1:]
                new_var_sample = random.sample(new_vars, len(old_vars))
                vars_used = vars_used | set(new_var_sample)
                var_map = list(zip(old_vars, new_var_sample))
                var_dict = dict(var_map)
                basename=os.path.splitext(os.path.basename(rule_file))[0]
                log.write(basename + " ")
                log.write(str(var_map))
                log.write("\n")

                formula = file.readline().rstrip().rstrip(";")
                pattern = re.compile("|".join(var_dict))
                conjuncts.append(pattern.sub(lambda m: var_dict[m.group(0)], formula))

    with open(output_file, 'w') as out:
        out.write("m2l-str;\n")
        out.write("var2 " + ", ".join(vars_used) + ";\n")
        out.write(" " + operator + " ".join(conjuncts) + ";\n")

def is_satisfiable(dfa_file):
    with open(dfa_file, 'r') as file:
        return 'unsatisfiable' not in file.read()

# Entry point
if __name__ == '__main__':

    # Check the correct number of command line arguments
    if len(sys.argv) < 8:
        print(usage())
        exit(-1)

    operator = sys.argv[1]
    random_seed = int(sys.argv[2])
    number_of_rules = int(sys.argv[3])
    number_of_patterns_per_rule = int(sys.argv[4])
    number_of_variables = int(sys.argv[5])
    output_format = sys.argv[6]
    log_format = sys.argv[7]
    dfa_format = sys.argv[8]
    pattern_files = sys.argv[9:]

    random.seed(random_seed)
    
    for i in range(number_of_rules):
        print("Rule %d" % i)

        new_vars = ['I%d' % i for i in range(number_of_variables)]
        output_file = output_format % i
        log_file = log_format % i
        dfa_file = dfa_format % i
        satisfiable = False

        while not satisfiable:
            samples = [ pattern_files[random.randrange(len(pattern_files))] for _ in range(number_of_patterns_per_rule) ]
            print("Generating formula...")
            generate_rule(samples, new_vars, output_file, log_file, operator)
            print("Constructing DFA...")
            os.system("mona -w -u %s > %s" % (output_file, dfa_file))
            satisfiable = is_satisfiable(dfa_file)

            if satisfiable:
                print("Rule is satisfiable, moving on")
            else:
                print("Rule is unsatisfiable, trying again")
