import json
import string

from os import listdir
from os.path import join

import numpy as np
import pandas as pd


def read_json(json_path):
    with open(json_path, 'r') as f_in:
        data = json.load(f_in)
    return data


def extension(filename):
    return filename.split('.')[-1]


def create_df(root_dir, categories_path, out_cvs):
    data = {}
    printable = set(string.printable)

    categories = read_json(categories_path)
    categories = [filter(lambda x: x in printable, category.replace(",", "_").replace(" ", "_")) for category in categories]

    for category in categories:
        data[category] = []

    json_files = [join(root_dir, name) for name in listdir(root_dir) if extension(name) == 'json']
    print len(json_files)
    for json_file in json_files:

        person_data = read_json(json_file)
        identity = filter(lambda x: x in printable, json_file.split('/')[-1].split('.')[0].replace(",", "_").replace(" ", "_"))

        for category in categories:
            if category not in person_data.keys():
                if category == 'identity':
                    data['identity'].append(identity)
                else:
                    data[category].append(np.NaN)
            else:
                if type(person_data[category]) == list:
                    if len(person_data[category]) > 0:
                        data[category].append(filter(lambda x: x in printable, person_data[category][0].replace(",", "").replace(" ", "_")))
                    else:
                        data[category].append(np.NaN)
                else:
                    data[category].append(filter(lambda x: x in printable, person_data[category].replace(",", "").replace(" ", "_")))

    print len(data['identity']), len(data['affiliation'])

    df = pd.DataFrame(data=data)
    df.to_csv(out_cvs, index=False)


def main():
    root_dir = '/home/joanna/studia/ekspertowe/se-guess-who/data/person_data/'
    categories_path = '/home/joanna/studia/ekspertowe/se-guess-who/data/categories.json'
    out_csv = '/home/joanna/studia/ekspertowe/se-guess-who/data/people_data.csv'
    create_df(root_dir, categories_path, out_csv)


if __name__ == '__main__':
    main()

