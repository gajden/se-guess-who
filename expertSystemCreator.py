import json

import sys
reload(sys)
sys.setdefaultencoding('UTF8')

# person_feats = ['gender', 'countryName', 'birthyear', 'occupation']
person_feats = ['gender', 'occupation']

aux_feats = ['domain', 'industry']

def create_prolog_code(data):
    code = ":- dynamic repl_yes/2, repl_no/2.\n"
    code += "\n\n"
    code += create_people_rules(data)
    code += "\n\n"
    code += reasoning_creator(data)
    code += "\n\n"
    code += add_ask()
    code += "\n\n"
    code += add_runner()
    return code


def person_creator(person):
    name = person['name'].replace(" ", "_").replace("'", "").replace(".","")
    rule_cmd = 'person_is({}) :- '.format(name)
    add_comma = False
    for feat in person_feats:
        feat_val = person[feat].replace(" ", "_")
        if feat_val is not None:
            if add_comma:
                rule_cmd += ", "
            else:
                add_comma = True
            rule_cmd += 'feature({}, {})'.format(feat, feat_val)
    rule_cmd += "."
    return rule_cmd

def create_people_rules(data):
    cmd = ""
    for person in data:
        cmd += person_creator(person) + "\n"
    return cmd

def reasoning_creator(data):
    cmd = ""
    deps = build_dep_tree(data)
    for dep in deps:
        for job in dep[2]:
            cmd += 'feature(occupation, {}) :- yes(domain, {}), yes(industry, {}), yes(occupation, {}).\n'\
                .format(job, dep[0], dep[1], job)

    domains = list(set([person['domain'] for person in data]))
    for dom in domains:
        cmd += ""

    cmd += "feature(gender, male) :- yes(gender, male).\n"
    cmd += "feature(gender, female) :- yes(gender, female).\n"

    return cmd

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

def get_data():
    f = open("people.json", 'r')
    json_data = f.read()
    data = json.loads(json_data)
    return data.values()

def get_test_data(data):
    return data[:100]

def build_dep_tree(data):
    domains = list(set([person['domain'].replace(" ", "_") for person in data]))

    deps = []

    for dom in domains:
        industries = list(set([person['industry'].replace(" ", "_") for person in data if person['domain'] == dom]))
        for ind in industries:
            jobs = list(set([person['occupation'].replace(" ", "_") for person in data if person['industry'] == ind]))
            deps.append([dom, ind, jobs])

    return deps

def main():
    data = get_data()
    test_data = get_test_data(data)

    code = create_prolog_code(test_data)

    out = open("test.pl", 'w')
    out.write(code)
    out.close()

main()