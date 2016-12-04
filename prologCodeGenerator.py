# -*- coding: utf-8 -*-

import os
import json
import re

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
        if get_single_person(f) is not None:
            all_data.append(get_single_person(f))
    return all_data


def get_single_person(file):
    fullpath = os.path.join("person_data", file)
    if os.path.exists(fullpath):
        f = open(fullpath, 'r')
        json_data = f.read()
        person_data = json.loads(json_data)
        cleaned_data = clear_null_info(person_data)
        name = file.replace(".json", "")
        return {'name': name, 'data': cleaned_data}
    return None


def clear_null_info(data):
    tmp_data = data.copy()
    for k, v in data.iteritems():
        if len(v) == 0:
            tmp_data.pop(k)
    return tmp_data


def create_prolog_code(data):
    code = ":- dynamic repl_yes/2, repl_no/2, not/1.\n"
    code += "\n\n"
    code += create_people_rules(data)
    code += "\n\n"
    code += get_all_countries(data)
    code += "\n\n"
    code += get_all_jobs(data)
    code += "\n\n"
    code += add_name_list(data)
    code += "\n\n"
    code += add_reasoning()
    code += "\n\n"
    code += add_ask()
    code += "\n\n"
    code += add_runner()
    return code

def add_reasoning():
    cmd = "basic_feats([sex_or_gender, occupation, country_of_citizenship]).\n" \
        "the_same(X,X).\n" \
        "reduce_list([H|T], X) :- the_same(H,X), length(T,0), !.\n" \
        "reduce_list(L, X) :- member(X,L), feature(X,Feat,Val), basic_feats(B), \+member(Feat, B), \+not(X), yes(Feat,Val), findall(A, feature(A, Feat, Val), L2), length(L2,1).\n" \
        "chosen(X) :- gender_ok(X), country_ok(X), occupation_ok(X).\n" \
        "gender_ok(X) :- genders(Gs), member(G, Gs), yes(sex_or_gender, G), feature(X, sex_or_gender, G).\n" \
        "country_ok(X) :- countries(Cs), member(C, Cs), yes(country_of_citizenship, C), feature(X, country_of_citizenship, C).\n" \
        "occupation_ok(X) :- occupations(Os), member(O, Os), yes(occupation, O), feature(X, occupation, O).\n" \
        "genders([male, female])."
    return cmd

def add_ask():
    cmd = "eval_answer(X,Y,y) :- assertz(repl_yes(X,Y)).\n" \
          "eval_answer(X,Y,n) :- assertz(repl_no(X,Y)), feature(P,X,Y), assertz(not(P)), fail.\n" \
          "ask_yes(X,Y) :- format('is ~w a/an ~w of the person? (y/n)~n',[Y,X]),\n" \
          "read(Reply),\n" \
          "eval_answer(X,Y,Reply).\n\n" \
          "yes(X,Y) :- repl_yes(X,Y).\n" \
          "yes(X,Y) :- \+repl_yes(X,_), \+repl_no(X,Y), ask_yes(X,Y).\n"
    return cmd


def add_runner():
    cmd = "clean :- retractall(repl_yes(_,_)), retractall(repl_no(_,_)), retractall(not(_)).\n"
    cmd += "person_is(Y) :- findall(X, chosen(X), L), reduce_list(L, Y).\n"
    cmd += "run :- person_is(X), format('~nIs it ~w ?~n', X).\n"
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
    cmd += "])."
    return cmd

def get_all_countries(data):
    cmd = "countries(["
    add_comma = False
    added = []
    frequency = {}
    for person in data:
        if 'country of citizenship' in person['data'].keys():
            country = person['data']['country of citizenship'][0]
            if country not in added:
                added.append(country)
                frequency[country] = 1
            else:
                frequency[country] += 1

    added = sorted(added, key=lambda cn: frequency[cn], reverse=True)

    for c in added:
        if add_comma:
            cmd += ", "
        else:
            add_comma = True
        cmd += safe_str(c)

    cmd += "])."
    return cmd


def get_all_jobs(data):
    cmd = "occupations(["
    add_comma = False
    frequency = {}
    added = []
    for person in data:
        if 'occupation' in person['data'].keys():
            for jb in person['data']['occupation']:
                if jb not in frequency.keys():
                    frequency[jb] = 1
                    added.append(jb)
                else:
                    frequency[jb] += 1

    added = sorted(added, key=lambda j: frequency[j], reverse=True)

    for job in added:
        if add_comma:
            cmd += ", "
        else:
            add_comma = True
        cmd += safe_str(job)

    cmd += "])."
    return cmd


def main():
    data = get_all_data()
    code = create_prolog_code(data)

    out = open("result.pl", 'w')
    out.write(code)
    out.close()

main()
