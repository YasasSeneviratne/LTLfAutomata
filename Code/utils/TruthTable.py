'''
The purpose of this module is to encode an automaton read from MONA's output in
binary and convert its transition function into a truth table for each state bit
'''

def from_dfa(mona_data):
    bit_length = (len(mona_data['states']) - 1).bit_length()
    
    input_names = mona_data['free_variables']
    old_state_names = ['old%d' % i for i in reversed(range(bit_length))]
    state_names = ['new%d' % i for i in reversed(range(bit_length))]

    tables = {s: [(input_names, old_state_names, s)] for s in state_names}

    state_format_string = '0%db' % bit_length
    label_format_string = '0%db' % len(input_names)

    for (source, dest), labels in mona_data['transition_dict'].items():
        binary_source = list(format(int(source), state_format_string))
        binary_dest = list(format(int(dest), state_format_string))

        for label in labels:
            binary_label = list(format(label, label_format_string))

            for i in range(bit_length):
                reverse_index = -(i + 1)
                row = (list(binary_label), list(binary_source), binary_dest[reverse_index])
                tables['new%d' % i].append(row)

    return tables

def from_nfa(mona_data):
    bit_length = len(mona_data['states'])
    
    input_names = mona_data['free_variables']
    old_state_names = ['old' + s for s in mona_data['states']]

    reverse_dict = {}

    def add_to_reverse_dict(dest, label, source):
        if dest not in reverse_dict:
            reverse_dict[dest] = {label: [source]}
        elif label not in reverse_dict[dest]:
            reverse_dict[dest][label] = [source]
        else:
            reverse_dict[dest][label].append(source)
    
    for (source, dest), labels in mona_data['transition_dict'].items():
        for label in labels:
            add_to_reverse_dict(dest, label, source)

    tables = {}
    label_format_string = '0%db' % len(input_names)

    for dest, labels_to_sources in reverse_dict.items():
        header = (input_names, old_state_names, 'new' + dest)
        table = [header]

        for label, sources in labels_to_sources.items():
            binary_label = format(label, label_format_string)
            next_row = ['X'] * bit_length
        
            for source in sources:
                source_index = int(source)
                next_row[source_index] = '1'
                table.append((binary_label, next_row.copy(), '1'))
                next_row[source_index] = '0'
            
            table.append((binary_label, next_row.copy(), '0'))
            
        tables[dest] = table

    return tables

def save_to_file(truth_tables, filename):
    try:
        with open(filename, 'w') as file:
            for truth_table in truth_tables.values():
                for (inputs, old_state_bits, new_state_bit) in truth_table:
                    file.write(' '.join(inputs) + ' : ' +
                               ' '.join(old_state_bits) + ' : ' +
                               new_state_bit + '\n')

                file.write('\n')
    except IOError as e:
        print("Exception: ", e)
