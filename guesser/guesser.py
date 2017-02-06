import pickle
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.models import BayesianModel
import pandas as pd
import numpy as np

input_file = 'artists_data.csv'

def create_data():

    data = open(input_file).readlines()

    res = {}

    feats = data[0].split(',')

    for feat in feats:
        res[feat.rstrip()] = []

    for person_idx in range(1, len(data)):
        personal_data = data[person_idx].split(',')
        for feat_idx in range(len(personal_data)):
            val = personal_data[feat_idx].rstrip()
            if val == '':
                val = '-'

            res[feats[feat_idx].rstrip()].append(val)
    return res


def probabilities(data, attrs, result):
    if type(data) == np.float64:
        result.append((attrs, data))
    else:
        length = len(data)
        for i in range(length):
            probabilities(data[i], attrs+[i], result)
    return result

def clean_probs(probs):
    return [p for p in probs if p[1] != 1./15]


def ask_question(attr_ind, cpd, prob):
    attr_name = cpd.variables[attr_ind]
    print "Select " + attr_name + ":"
    res_no = 0
    avail_answers = [x[0][attr_ind] for x in prob]
    for res in cpd.state_names[attr_name]:
        if res_no in avail_answers:
            print str(res_no) + ":  " + res
        res_no += 1
    response = raw_input("> ")
    return int(response)


def reduce_probs(probs, response, attr_ind):
    probs_red = [p for p in probs if p[0][attr_ind] == response]
    return probs_red


def print_temp_results(probs, names):
    print len(probs)
    person_probs = []
    for person_idx in range(15):
        person_probs.append(sum([p[1] for p in probs if p[0][0] == person_idx]))
    sum_probs = sum(person_probs)
    if sum_probs > 0:
        probs = [p/sum_probs for p in person_probs]
    result_count = 0
    if len(probs) == 0:
        print "\nNO MATCHES"
        exit(0)
    print
    for person_idx in range(15):
        if probs[person_idx] > 0:
            result_count += 1
            print names[person_idx], probs[person_idx]
    print
    if result_count < 2:
        exit(0)


def guess(probs, names, cpd):
    probs = clean_probs(probs)
    for j in range(1, 8):
        i = 9-j
        response = ask_question(i, cpd, probs)
        probs = reduce_probs(probs, response, i)
        print_temp_results(probs, names)



"""
data = create_data()
print data
inp = pd.DataFrame(data=data)



with open('graph_50.pkl', 'rb') as f:
    graph = pickle.load(f)

new_graph = []
data = open(input_file).readlines()
feats = data[0].split(',')

for feat in feats:
    if feat == 'identity':
        continue
    new_graph.append((feat.rstrip(), 'identity'))

model = BayesianModel(new_graph)
print model.edges()

mle = MaximumLikelihoodEstimator(model, inp)
print "mle done"

params = mle.estimate_cpd('identity')
model_dump = open('model_dump.pkl', 'wb')
pickle.dump(params, model_dump)
model_dump.close()
"""


with open("model_dump_15.pkl", 'rb') as f:
    params = pickle.load(f)


probs = probabilities(params.values, [], [])
names = params.state_names['identity']

guess(probs, names, params)

# f_out = open("out.txt", "w")
# f_out.write(str(params))
# f_out.close()
