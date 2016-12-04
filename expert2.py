# -*- coding: utf-8 -*-

import os
import json
import re
import itertools

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

def get_feature_list(all_data):
    allkeys = []
    for d in all_data:
        for k in d['data'].keys():
            allkeys.append(k)
    return list(set(allkeys))


def create_people_rules(data):
    cmd = ""
    for person in data:
        cmd += person_creator(person) + "\n"
    return cmd


def safe_str(string):
    s = re.sub('[^0-9a-zA-Z]+', '_', string).lower()
    if s[0].isdigit():
        s = "x_"+s
    elif s[0] == "_":
        s = "x"+s
    return s


def person_creator(person):
    name = safe_str(person['name'])
    rule_cmd = ''
    person_feats = person['data'].keys()
    for feat in person_feats:
        feat_val = person['data'][feat]
        for v in feat_val:
            rule_cmd += 'feature({}, {}, {}).\n'.format(name, safe_str(feat), safe_str(v))
    return rule_cmd


def get_all_data():
    all_data = []
    fls = os.listdir('person_data')
    for f in fls:
        all_data.append(get_single_person(f))
    return all_data


def get_single_person(file):
    fullpath = os.path.join("person_data", file)
    f = open(fullpath, 'r')
    json_data = f.read()
    person_data = json.loads(json_data)
    cleaned_data = clear_null_info(person_data)
    name = file.replace(".json", "")
    return {'name': name, 'data': cleaned_data}


def clear_null_info(data):
    tmp_data = data.copy()
    for k, v in data.iteritems():
        if len(v) == 0:
            tmp_data.pop(k)
    return tmp_data


def create_prolog_code(data):
    code = ":- dynamic repl_yes/2, repl_no/2.\n"
    code += "\n\n"
    code += create_people_rules(data)
    code += "\n\n"
    # code += reasoning_creator(data)
    # code += "\n\n"
    code += add_name_list(data)
    code += "\n\n"
    code += add_ask()
    code += "\n\n"
    code += add_runner()
    return code


def add_ask():
    cmd = "eval_answer(X,Y,y) :- assertz(repl_yes(X,Y)), writeln('Y').\n" \
          "eval_answer(X,Y,n) :- assertz(repl_no(X,Y)), writeln('N'), fail.\n\n" \
          "ask_yes(X,Y) :- format('is ~w a/an ~w of the person? (y/n)~n',[Y,X]),\n" \
          "read(Reply),\n" \
          "eval_answer(X,Y,Reply).\n\n" \
          "yes(X,Y) :- repl_yes(X,Y).\n" \
          "yes(X,Y) :- \+repl_yes(X,_), \+repl_no(X,Y), ask_yes(X,Y).\n"
    return cmd


def add_runner():
    cmd = "clean :- retractall(repl_yes(_,_)), retractall(repl_no(_,_)).\n"
    cmd += "run :- person_is(X), format('~nIs it ~w ?~n', X), clean.\n"
    cmd += "run :- write('I dont know'), clean.\n"
    return cmd

def add_name_list(data):
    cmd = "name_list(["
    add_comma = False
    for person in data:
        if add_comma:
            cmd += ", "
        else:
            add_comma = True
        cmd += safe_str(person['name'])
    cmd += "])"
    return cmd


def main():
    data = get_all_data()
    code = create_prolog_code(data)

    out = open("test2.pl", 'w')
    out.write(code)
    out.close()

main()