# !/usr/bin/venv
# -*- coding: utf-8 -*-

import csv
from matplotlib import pyplot as plt

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

def cleanup_dates(data: dict):
    AGE_VALS = {
        'FA': 0,
        'SA': 4902,
        'TA': 8343,
    }

    # Repeat for every character
    for line in data.values():
        yots = 0 # yots = Years of the Sun // not used //
        
        # Find the yots value for the birth and death
        for t in ['birth', 'death']:
            # Repeat for every age text: k and age val: v
            for k, v in AGE_VALS.items():
                if k in line[t]:
                    # Except if the age text is not in the birth/death year
                    try:
                        line[t] = int(line[t].replace(k + ' ', '')) + v
                        break
                    except ValueError:
                        pass
            
            # Find lifespan
            try:
                line['lifespan'] = line['death'] - line['birth']
            except TypeError:
                pass

    return data

def plot_points_scatter(data: dict, fig_name):
    RACES = {
        'Elves': ['Elves', 'Elf', 'Half-elven', 'Elves,Noldor'],
        'Men': ['Men', 'Men,Rohirrim', 'Drúedain'],
        'Dragons': ['Dragon', 'Dragons'],
        'Hobbits': ['Hobbits', 'Hobbit'],
        'Dwarves': ['Dwarves', 'Dwarven', 'Dwarf'],
        'Monsters': ['Orcs', 'Great Spiders', 'Black Uruk', 'Balrog', 'Werewolves', 'Goblin,Orc', 'Orc', 'Uruk-hai']
    }

    RACE_COLORS = {
        'Elves': 'yellow',
        'Men': 'blue',
        'Dragons': 'orange',
        'Hobbits': 'green',
        'Dwarves': 'grey',
        'Monsters': 'red'
    }

    race_lists = {}

    # Repeat for every race
    for race in RACES:
        race_lists[race] = [[], []] 
        
        # Repeat for every character's data
        for line in data.values():
            if line['race'] in RACES[race]:
                # Except if the character does not have a valid lifespan
                try:
                    # Remove edge cases/outliers
                    if line['lifespan'] < 0: continue
                    if line['lifespan'] > 1000: continue

                    # Add data to race_lists
                    race_lists[race][1].append(line['lifespan'])
                    race_lists[race][0].append(line['birth'])
                except KeyError:
                    pass
        
        # Init scatter for every race
        plt.scatter(race_lists[race][0], race_lists[race][1], c=RACE_COLORS[race], s=10)

    # Graphing stuff
    plt.xlabel('Years of the Sun')
    plt.ylabel('Lifespan')
    plt.legend(RACE_COLORS)
    plt.savefig(fig_name)

def plot_points_bar(data: dict, fig_name):
    AGE_VALS = {
        'First Age': [0, 4902],
        'Second Age': [4902, 8343],
        'Third Age': [8343, 11364],
    }

    SUB_RACES = {
        'Hobbits': ['Hobbits', 'Hobbit'],
        'Dwarves': ['Dwarves', 'Dwarven', 'Dwarf'],
    }

    race_lifespans = {
        'Hobbits': [],
        'Dwarves': [],
        'Men': [],
        'Men\nFirst Age': [],
        'Men\nSecond Age': [],
        'Men\nThird Age': [],
    }

    # Parse men and add them to the correct buckets
    for age, year in AGE_VALS.items():
        for line in data.values():
            if 'men' in line['race'].lower():
                try:
                    race_lifespans['Men'].append(line['lifespan'])
                except KeyError:
                    pass

                try:
                    if int(line['birth']) > year[0] and int(line['birth']) < year[1]:
                        race_lifespans[f'Men\n{age}'].append(line['lifespan'])
                except TypeError:
                    pass
                except ValueError:
                    pass
                except KeyError:
                    pass

    # Add hobbits to hobbit bucket
    for line in data.values():
        if line['race'] in SUB_RACES['Hobbits']:
            try:
                race_lifespans['Hobbits'].append(line['lifespan'])
            except KeyError:
                pass
    
    # Add dwarves to dwarven bucket
    for line in data.values():
        if line['race'] in SUB_RACES['Dwarves']:
            try:
                race_lifespans['Dwarves'].append(line['lifespan'])
            except KeyError:
                pass

    # Calculate average lifespan for each race
    for race, lifespans in race_lifespans.items():
        race_lifespans[race] = sum(lifespans) / len(lifespans)

    # Generate bar graph fig subplot
    fig = plt.figure()
    fig.clf()
    ax = fig.add_subplot(111)

    # Graphing stuff
    plt.bar(race_lifespans.keys(), race_lifespans.values(), color='#747574')
    plt.setp(ax.get_xticklabels(), fontsize=7)
    plt.ylabel('Life Expectancy')
    plt.savefig(fig_name)

def main():
    # Load data
    data, header = load_csv('Assets/lotr_characters.csv')

    # Change data into a dict
    dict_data = dictify_data(data, header)

    # Change format of dates to YOTS. eg: SA 2150 = 7052 (yots)
    dict_data = cleanup_dates(dict_data)

    # Create scatter plot
    plot_points_scatter(dict_data, 'scatter.png')

    # Create bar plot
    plot_points_bar(dict_data, 'bar.png')

if __name__ == '__main__':
    main()