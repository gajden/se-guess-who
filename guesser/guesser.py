import pickle
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.models import BayesianModel
import pandas as pd
import numpy as np

input_file = 'artists_data.csv'

def create_data():

    # data = open('people_data.csv').readlines()
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

def writer(data, attrs):
    if type(data) == np.float64:
        print attrs+": "+str(data)
    else:
        length = len(data)
        for i in range(length):
            writer(data[i], attrs+str(i)+".")


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
print type(params)
print [f for f in dir(params) if not f.startswith("_")]

print params.variables
print params.cardinality

writer(params.values, "")

f_out = open("out.txt", "w")
f_out.write(str(params))
f_out.close()
