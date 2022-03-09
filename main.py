# !/usr/bin/venv
# -*- coding: utf-8 -*-

import csv

def load_csv(path):
    with open(path, 'r') as f:
        data = list(csv.reader(f))

    header = data.pop(0)
    return data, header
    
def print_data(data, header):
    # Define template from header
    template = '{%s:<}' % (header[0])

    for title in header[1:]:
        template += ' | {%s:<}' % (title)

    # Print the data rows
    for data_row in data:
        # Convert the data row into a dict format
        
        d = {header[i]: piece for i, piece in enumerate(data_row)}
        row = template.format(**d)
        print(row)

def dictify_data(data: list, header, name='name'):
    # Create the header dict : {'birth': 0, 'death': 1...}
    header_dict = {v: k for k, v in dict(enumerate(header)).items()}

    dict_data = {}

    # Create dict_data: Beren: {'birth': 'FA 432', 'death': 'FA 466', 'gender': 'Male', 'hair': 'Dark'...}
    for line in data:
        dict_data[line[header_dict[name]]] = {k: line[v] for k, v in header_dict.items()}
    
    return dict_data

def cleanup_dates(data: dict, dates=['birth', 'death']):
    AGE_VALS = {
        'FA': 4902,
        'SA': 3441,
        'TA': 3021
    }

    for line in data.values():
        for age_name, age_val in AGE_VALS.items(5):
            pass



def main():
    data, header = load_csv('Assets/lotr_characters.csv')

    # print_data(data, header)

    dict_data = dictify_data(data, header)

    # for name, line in dict_data.items():
        # print(f'{name}: {line}')

    print(dict_data['Beren'])


if __name__ == '__main__':
    main()